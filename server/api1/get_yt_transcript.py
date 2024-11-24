import subprocess
import os
import glob
import srt
import json
from colorama import Fore

def fetch_and_save_transcript(video_url, output_file='transcript.srt'):
    """
    Fetches YouTube transcript using yt-dlp, converts it to SRT, 
    and saves it as the specified output file.
    
    Args:
        video_url (str): The URL of the YouTube video.
        output_file (str): The name of the output SRT file. Default is 'transcript.srt'.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Remove existing output file
        if os.path.exists(output_file):
            os.remove(output_file)
            print(Fore.YELLOW + f"Existing {output_file} deleted.")

        # Run yt-dlp to download subtitles
        subprocess.run([
            'yt-dlp',
            '--write-auto-sub',
            '--convert-subs=srt',
            '--skip-download',
            video_url
        ], check=True)

        # Find all .srt files in the current directory
        srt_files = glob.glob('*.srt')

        if not srt_files:
            print(Fore.RED + "Error: No .srt file was generated.")
            return False

        # Rename the first SRT file to the desired output file
        os.rename(srt_files[0], output_file)
        print(Fore.GREEN + f"Transcript saved as {output_file}")

        # Remove any other SRT files (cleanup)
        for extra_file in srt_files[1:]:
            os.remove(extra_file)
            print(Fore.YELLOW + f"Removed extra SRT file: {extra_file}")

        return True
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error running yt-dlp: {e}")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
    return False


def srt_to_custom_json(srt_file, json_file):
    """Converts SRT to custom JSON format."""
    try:
        with open(srt_file, 'r', encoding='utf-8') as f:
            srt_content = f.read()

        # Parse the SRT content
        subtitles = list(srt.parse(srt_content))

        # Prepare the data in the required JSON format
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

        # Save the data as JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
        print(Fore.WHITE + f"Successfully converted SRT to JSON: {json_file}")
        return True
    except Exception as e:
        print(Fore.RED + f"Error converting SRT to JSON: {str(e)}")
        return False


# Example usage
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    fetch_and_save_transcript(video_url)
    srt_to_custom_json("transcript.srt", "transcript.json")
