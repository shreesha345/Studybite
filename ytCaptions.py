import subprocess
import os
import glob

def fetch_and_save_transcript(video_url, output_file='transcript.srt'):
    try:
        # Run yt-dlp command with corrected ffmpeg location
        subprocess.run([
            'yt-dlp',
            '--write-auto-sub',
            '--convert-subs', 'srt',
            '--skip-download',
            '--ffmpeg-location', 'C:\\ffmpeg',
            video_url
        ], check=True)

        # Find the generated .srt file
        srt_files = glob.glob('*.srt')
        if not srt_files:
            print("Error: No .srt file was generated.")
            return

        # Rename the first .srt file found to the specified output file
        os.rename(srt_files[0], output_file)
        print(f"Transcript saved as {output_file}")

        # Clean up any other .srt files if multiple were generated
        for file in srt_files[1:]:
            os.remove(file)

    except subprocess.CalledProcessError as e:
        print(f"Error running yt-dlp: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    fetch_and_save_transcript(video_url)
