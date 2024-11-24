from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import logging
from get_yt_transcript import fetch_and_save_transcript
from video_reader import gemini_insights
from video_segment import trim_video
from dub import main_dub
import yt_dlp
import json
import srt
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv('.env')

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoProcessRequest(BaseModel):
    url: str
    topic: str
    languageCode: str

def srt_to_custom_json(srt_file, json_file):
    """Converts SRT to custom JSON format."""
    try:
        logger.info(f"Reading SRT file: {srt_file}")
        with open(srt_file, 'r', encoding='utf-8') as f:
            srt_content = f.read()

        logger.info("Parsing SRT content")
        subtitles = list(srt.parse(srt_content))
        data = []
        for sub in subtitles:
            start_seconds = sub.start.total_seconds()
            end_seconds = sub.end.total_seconds()
            duration = round(end_seconds - start_seconds, 2)

            entry = {
                "start_time": round(start_seconds, 2),
                "end_time": round(end_seconds, 2),
                "description": sub.content.strip(),
                "duration": duration
            }
            data.append(entry)

        logger.info(f"Writing JSON file: {json_file}")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
        logger.info("Successfully converted SRT to JSON")
        return True
    except Exception as e:
        logger.error(f"Error converting SRT to JSON: {str(e)}")
        raise Exception(f"Failed to convert SRT to JSON: {str(e)}")

def download_youtube_video(link):
    """Download a YouTube video."""
    try:
        video_file = "input.mp4"
        
        if os.path.exists(video_file):
            logger.info(f"File '{video_file}' already exists. Deleting it.")
            os.remove(video_file)

        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': video_file,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'noprogress': False,
        }
        
        logger.info("Starting video download")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        if not os.path.exists(video_file):
            raise Exception("Video file was not created after download")
            
        logger.info("Video download completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        raise Exception(f"Failed to download video: {str(e)}")

@app.post("/process-video")
async def process_video(request: VideoProcessRequest):
    """Process a YouTube video"""
    url = request.url
    topic = request.topic
    languageCode = request.languageCode
    output_clips_folder = 'Clips'

    try:
        # Ensure Clips directory exists
        os.makedirs(output_clips_folder, exist_ok=True)
        logger.info(f"Created/verified output directory: {output_clips_folder}")

        # Step 1: Download and process transcript
        logger.info("Starting transcript download")
        transcript_result = fetch_and_save_transcript(url, output_file='transcript.srt')
        if not transcript_result:
            raise HTTPException(status_code=500, detail="Failed to fetch transcript")
        logger.info("Transcript downloaded successfully")

        # Verify transcript file exists
        if not os.path.exists('transcript.srt'):
            raise HTTPException(status_code=500, detail="Transcript file not found after download")
        
        logger.info("Converting transcript to JSON")
        json_result = srt_to_custom_json('transcript.srt', 'transcript.json')
        if not json_result:
            raise HTTPException(status_code=500, detail="Failed to convert transcript to JSON")
        logger.info("Transcript converted to JSON successfully")

        # Step 2: Download video
        logger.info("Starting video download")
        video_result = download_youtube_video(url)
        if not video_result:
            raise HTTPException(status_code=500, detail="Failed to download video")
        logger.info("Video downloaded successfully")

        # Step 3: Extract insights
        logger.info("Starting insights extraction")
        insights_result = gemini_insights(topic)
        if not insights_result:
            raise HTTPException(status_code=500, detail="Failed to extract insights")
        logger.info("Insights extracted successfully")

        # Verify segments file exists
        if not os.path.exists('best_segments.json'):
            raise HTTPException(status_code=500, detail="Segments file not found after insights extraction")

        # Step 4: Trim video segments
        logger.info("Starting video trimming")
        trim_result = trim_video('input.mp4', 'best_segments.json', output_clips_folder)
        if not trim_result:
            raise HTTPException(status_code=500, detail="Failed to trim video segments")
        logger.info("Video segments trimmed successfully")

        # Step 5: Translate and dub
        logger.info("Starting video dubbing")
        apiKey = os.getenv('11_LABS')
        if not apiKey:
            raise HTTPException(status_code=500, detail="ElevenLabs API key not found")
        
        dub_result = main_dub(apiKey, languageCode)
        if not dub_result:
            raise HTTPException(status_code=500, detail="Failed to dub video")
        logger.info("Video dubbing completed successfully")

        # Check output files
        output_files = os.listdir(output_clips_folder)
        if not output_files:
            raise HTTPException(status_code=404, detail="No processed videos found")
        
        logger.info(f"Processing completed. Found {len(output_files)} output files")
        return {
            "message": "Video processing completed successfully!",
            "files": output_files
        }

    except HTTPException as he:
        logger.error(f"HTTP Exception: {str(he.detail)}")
        raise he
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-video/{filename}")
async def download_video(filename: str):
    """Download a processed video file."""
    file_path = os.path.join("output", filename)
    
    if not os.path.exists("output"):
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail=f"File {filename} not found")

    logger.info(f"Serving file: {file_path}")
    return FileResponse(file_path, media_type="video/mp4", filename=filename)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
