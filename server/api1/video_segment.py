import json
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def trim_video(input_file, parts_file, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load the parts from the JSON file
    with open(parts_file, 'r') as f:
        parts = json.load(f)
    
    # Load the input video
    video = VideoFileClip(input_file)
    
    # Process each part and save the clips
    for index, part in enumerate(parts):
        start_time = part['start_time']
        end_time = part['end_time']
        duration = end_time - start_time
        
        # Trim the video for the given start and end times
        clip = video.subclip(start_time, end_time)
        
        # Generate the output file name
        output_file = os.path.join(output_folder, f'clip_{index + 1}.mp4')
        
        # Write the clip to a file
        clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
        
        print(f'Saved {output_file}')
    
    # Close the video file
    video.close()
    return "process completed"


# if __name__=='__main__':
# # # Define file paths
#     input_video = '/kaggle/working/input.mp4'
#     parts_json = '/kaggle/working/best_segments.json'
#     output_clips_folder = '/kaggle/working/Clips'

#     # Call the function
#     trim_video(input_video, parts_json, output_clips_folder)