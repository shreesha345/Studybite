from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from starlette.background import BackgroundTask
from elevenlabs import ElevenLabs
import time
import moviepy.editor as me
import os
import shutil
from contextlib import contextmanager

app = FastAPI()

@contextmanager
def video_clip_manager(*clips):
    """Context manager to ensure proper cleanup of video clips."""
    try:
        yield clips
    finally:
        for clip in clips:
            try:
                clip.close()
            except Exception:
                pass

def wait_for_dubbing_completion(dubbing_id: str, client: ElevenLabs, max_attempts: int = 120, check_interval: int = 10) -> bool:
    for attempt in range(max_attempts):
        metadata = client.dubbing.get_dubbing_project_metadata(dubbing_id)
        if metadata.status == "dubbed":
            return True
        elif metadata.status == "dubbing":
            print(f"Dubbing in progress... Attempt {attempt + 1}/{max_attempts}")
            time.sleep(check_interval)
        else:
            print("Dubbing failed:", metadata.error_message)
            return False
    
    print("Dubbing timed out.")
    return False

def dub_video(input_path: str, api_key: str, target_language_code: str) -> str:
    client = ElevenLabs(api_key=api_key)
    temp_output_name = "temp_output.mp4"
    final_output_name = "output.mp4"
    
    try:
        with open(input_path, "rb") as video_file:
            dub = client.dubbing.dub_a_video_or_an_audio_file(
                target_lang=target_language_code,
                file=video_file,
                watermark=True
            )
        
        dubbing_id = dub.dict()["dubbing_id"]

        if not wait_for_dubbing_completion(dubbing_id, client):
            raise Exception("Dubbing process failed or timed out.")

        print("Downloading the dubbed video...")
        with open(temp_output_name, "wb") as f:
            for chunk in client.dubbing.get_dubbed_file(dubbing_id, target_language_code):
                f.write(chunk)
        
        # Use context manager for video clips
        with video_clip_manager(
            me.VideoFileClip(input_path),
            me.VideoFileClip(temp_output_name)
        ) as (original_video_clip, dubbed_video_clip):
            original_video_clip.audio = dubbed_video_clip.audio
            original_video_clip.write_videofile(final_output_name, codec="libx264")

        return final_output_name
    
    finally:
        # Clean up intermediate file
        if os.path.exists(temp_output_name):
            try:
                os.remove(temp_output_name)
            except Exception as e:
                print(f"Failed to remove temporary file: {e}")

def cleanup_files(*files):
    """Enhanced cleanup function with retry mechanism."""
    max_retries = 3
    retry_delay = 1  # seconds
    
    for file in files:
        if not os.path.exists(file):
            continue
            
        for attempt in range(max_retries):
            try:
                os.remove(file)
                break
            except PermissionError:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                print(f"Failed to remove {file} after {max_retries} attempts")
            except Exception as e:
                print(f"Error removing {file}: {e}")
                break

@app.post("/upload")
async def upload_video(
    video: UploadFile = File(...),
    api_key: str = Form(...),
    target_lang: str = Form(...)
):
    input_file = "input.mp4"
    try:
        with open(input_file, "wb") as f:
            f.write(video.file.read())
        
        output_file = dub_video(input_file, api_key, target_lang)
        
        return FileResponse(
            output_file,
            media_type="video/mp4",
            filename="output.mp4",
            background=BackgroundTask(cleanup_files, input_file, output_file)
        )
    except Exception as e:
        # Clean up input file if something goes wrong
        if os.path.exists(input_file):
            cleanup_files(input_file)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <body>
            <h1>Video Dubbing API</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="video" required><br>
                <input type="text" name="api_key" placeholder="ElevenLabs API Key" required><br>
                <input type="text" name="target_lang" placeholder="Target Language Code (e.g., en-IN)" required><br>
                <button type="submit">Upload and Dub</button>
            </form>
        </body>
    </html>
    """