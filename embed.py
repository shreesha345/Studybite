import subprocess
import os

def downloadSegment(ytVideoUrl: str, ts1: str = "00:00:00", ts2: str = "00:01:00"):
    '''
    downloads a segment of video and return the output file name
    '''
    # Delete the file named output.mp4 so that it allows yt-dlp to write with the same name
    if os.path.exists("output.mp4"):
        os.remove("output.mp4")
    
    # Run the yt-dlp cli command
    subprocess.run([
        "yt-dlp",
        "-f","mp4",
        "-S", "res:720",
        "--download-sections", f"*{ts1}-{ts2}",
        "-o", "output.mp4",
        ytVideoUrl
    ],check=True)
    
def writeDemoHtml(videoFilename: str):
    '''
    Writes a demo html code to test the video embedding
    '''
    demoTemplate='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    Youtube Video
    <video width="560" height="315" controls>
        <source src={}>
    </video>
</body>
</html>'''
    outputFileName = "embedTest.html"
    with open(outputFileName,"w") as f:
        f.write(demoTemplate.format(videoFilename))
    print(f"Demo code written in {outputFileName}")
    
url = input("Enter a youtube video url: ")
ts1 = input("Enter start timestamp:  ")
ts2 = input("Enter end timestamp: ")
print("Segment of the video is downloading...:\n")
downloadSegment(url, ts1, ts2)
writeDemoHtml("output.mp4")