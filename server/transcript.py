import subprocess
import os
import glob
from colorama import Fore

def fetch_transcript(video_url):
    """
    Fetches the transcript for a YouTube video and returns it as a string.
    
    Parameters:
        video_url (str): The URL of the YouTube video.
    
    Returns:
        str: The cleaned transcript, or None if an error occurs.
    """
    try:
        # Run yt-dlp command to fetch transcript
        subprocess.run([
            'yt-dlp',
            '--write-auto-sub',
            '--convert-subs=srt',
            '--skip-download',
            video_url
        ], check=True)

        # Find the generated .srt file
        srt_files = glob.glob('*.srt')
        if not srt_files:
            print(Fore.RED + "Error: No transcript file was generated.")
            return None

        # Read and process the .srt file
        with open(srt_files[0], 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic cleanup of the SRT content
        lines = content.split('\n')
        transcript_lines = []
        
        for line in lines:
            # Skip empty lines, timestamp lines, and sequence numbers
            if not line.strip():
                continue
            if '-->' in line:
                continue
            if line.strip().isdigit():
                continue

            # Add non-empty lines that aren't timestamps or numbers
            cleaned_line = line.strip()
            if cleaned_line:
                transcript_lines.append(cleaned_line)

        # Clean up the .srt file
        for file in srt_files:
            os.remove(file)
            print(Fore.WHITE + f"Removed temporary file: {file}")

        # Return the cleaned transcript as a string
        return " ".join(transcript_lines)

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error running yt-dlp: {e}")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
    
    return None