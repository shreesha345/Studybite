from elevenlabs import ElevenLabs
import time
import moviepy.editor as me
import os

def wait_for_dubbing_completion(dubbing_id: str, client) -> bool:
    """
    Waits for the dubbing process to complete by periodically checking the status.

    Args:
        dubbing_id (str): The dubbing project id.
        client: Your client object

    Returns:
        bool: True if the dubbing is successful, False otherwise.
    """
    MAX_ATTEMPTS = 120
    CHECK_INTERVAL = 10  # In seconds

    for attempt in range(MAX_ATTEMPTS):
        try:
            metadata = client.dubbing.get_dubbing_project_metadata(dubbing_id)
            if metadata.status == "dubbed":
                return True
            elif metadata.status == "dubbing":
                print(
                    f"Dubbing in progress... Attempt {attempt + 1}/{MAX_ATTEMPTS}. Will check status again in",
                    CHECK_INTERVAL,
                    "seconds.",
                )
                time.sleep(CHECK_INTERVAL)
            else:
                print("Dubbing failed:", metadata.error_message)
                return False
        except Exception as e:
            print(f"Error checking dubbing status: {e}")
            return False

    print("Dubbing timed out")
    return False

def validate_video_file(video_path: str) -> bool:
    """
    Validates if the video file exists and can be opened by MoviePy.
    
    Args:
        video_path (str): Path to the video file
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            return False
            
        clip = me.VideoFileClip(video_path)
        if clip.reader is None:
            print(f"Cannot read video file: {video_path}")
            clip.close()
            return False
            
        clip.close()
        return True
    except Exception as e:
        print(f"Error validating video file {video_path}: {e}")
        return False

def dub_video(video_file_name: str, elevenlabs_api_key: str, target_language_code: str, output_dir: str):
    '''
    Dubs the given video and saves the dubbed version in the output directory.

    Parameters:
    video_file_name: name of the input video file
    elevenlabs_api_key: your generated 11 labs api key
    target_language_code: language code of the target language
    output_dir: directory to save the output video
    '''
    if not validate_video_file(video_file_name):
        return False

    client = ElevenLabs(api_key=elevenlabs_api_key)
    try:
        with open(video_file_name, "rb") as video_file:
            dub = client.dubbing.dub_a_video_or_an_audio_file(
                target_lang=target_language_code,
                file=video_file,
                watermark=True
            )
    except Exception as e:
        print(f"Error initiating dubbing: {e}")
        return False

    dubbing_id = dub.dict()["dubbing_id"]
    if not wait_for_dubbing_completion(dubbing_id, client):
        return False

    print(f"Downloading the dubbed video for {video_file_name}...")
    dubbed_video_path = os.path.join(output_dir, f"dubbed-{os.path.basename(video_file_name)}")
    
    # Download the dubbed video
    try:
        with open(dubbed_video_path, "wb") as f:
            for chunk in client.dubbing.get_dubbed_file(dubbing_id, target_language_code):
                f.write(chunk)
    except Exception as e:
        print(f"Error downloading dubbed video: {e}")
        return False

    # Validate the dubbed video file
    if not validate_video_file(dubbed_video_path):
        print("Downloaded dubbed video is invalid")
        return False

    original_video_clip = None
    dubbed_video_clip = None

    try:
        # Sync audio to the original video
        original_video_clip = me.VideoFileClip(video_file_name)
        dubbed_video_clip = me.VideoFileClip(dubbed_video_path)

        # Validate both clips
        if original_video_clip.reader is None or dubbed_video_clip.reader is None:
            raise ValueError("Failed to load video clips")

        if dubbed_video_clip.audio is None:
            raise ValueError("Dubbed video has no audio track")

        original_video_clip.audio = dubbed_video_clip.audio
        output_video_path = os.path.join(output_dir, f"{os.path.basename(video_file_name)}")
        
        # Write the final video
        original_video_clip.write_videofile(
            output_video_path,
            codec="libx264",
            audio_codec="aac",
            logger=None  # Suppress MoviePy's progress bar
        )
        
        print(f"Dubbed video saved to {output_video_path}")
        return True
        
    except Exception as e:
        print(f"Error during video processing: {e}")
        return False
        
    finally:
        # Clean up resources
        try:
            if original_video_clip is not None:
                original_video_clip.close()
            if dubbed_video_clip is not None:
                dubbed_video_clip.close()
            if os.path.exists(dubbed_video_path):
                os.remove(dubbed_video_path)
        except Exception as e:
            print(f"Error during cleanup: {e}")

def main_dub(api_key, language_code):
    if not api_key:
        print("Error: API key is required")
        return "Error: API key is required"
        
    if not language_code:
        print("Error: Language code is required")
        return "Error: Language code is required"

    clips_folder = "Clips"
    output_folder = "output"

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    success_count = 0
    failure_count = 0

    # Process each video in the Clips folder
    if os.path.exists(clips_folder) and os.path.isdir(clips_folder):
        video_files = [f for f in os.listdir(clips_folder) 
                      if f.endswith((".mp4", ".mov"))]
        
        if not video_files:
            message = f"No video files found in {clips_folder}"
            print(message)
            return message

        for video_file in video_files:
            video_path = os.path.join(clips_folder, video_file)
            print(f"\nProcessing {video_file}...")
            try:
                if dub_video(video_path, api_key, language_code, output_folder):
                    success_count += 1
                else:
                    failure_count += 1
            except Exception as e:
                print(f"Error processing {video_file}: {e}")
                failure_count += 1
                
        message = f"Processing complete. Successfully dubbed: {success_count}, Failed: {failure_count}"
        print(message)
        return message
    else:
        message = f"No Clips folder found at {clips_folder}"
        print(message)
        return message

if __name__ == "__main__":
    main_dub(api_key='sk_6d05a3ea8ab6987a531768782112fe6b1cd15f746c83ebf7', language_code='hi')