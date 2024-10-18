from elevenlabs import ElevenLabs
import time
import moviepy.editor as me
import os

# This function was copied from official elevenlabs github repo
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

    for _ in range(MAX_ATTEMPTS):
        metadata = client.dubbing.get_dubbing_project_metadata(dubbing_id)
        if metadata.status == "dubbed":
            return True
        elif metadata.status == "dubbing":
            print(
                "Dubbing in progress... Will check status again in",
                CHECK_INTERVAL,
                "seconds.",
            )
            time.sleep(CHECK_INTERVAL)
        else:
            print("Dubbing failed:", metadata.error_message)
            return False


    print("Dubbing timed out")
    return False

def dubVideo(videoFileName: str, elevenlabsApiKey: str, targetLanguageCode: str):
    '''
    Dubs the given video and dubs it into target language
    Parameters:
    videoFilename: name of the input video file
    elevenlabsApiKey: your generated 11 labs api key
    targetLanguageCode: language code of the target language
    '''
    client = ElevenLabs(api_key=elevenlabsApiKey)
    videoFile = open(videoFileName, "rb")
    dub = client.dubbing.dub_a_video_or_an_audio_file(
        target_lang=targetLanguageCode,
        file=videoFile,
        watermark=True
    )
    
    print(dub)
    
    dubbingId = dub.dict()["dubbing_id"]
    outputVideoName = f"output-{targetLanguageCode}.mp4"
    
    if wait_for_dubbing_completion(dubbingId, client):
        print("Downloading the dubbed video...")
        with open(outputVideoName, "wb") as f:
            for chunk in client.dubbing.get_dubbed_file(dubbingId, targetLanguageCode):
                f.write(chunk)
    
    originalVideoClip = me.VideoFileClip("input.mp4")
    dubbedVideoClip = me.VideoFileClip(f"output-{targetLanguageCode}.mp4")
    
    dubbedAudioClip = dubbedVideoClip.audio
    originalVideoClip.audio = dubbedAudioClip
    
    os.remove(outputVideoName)
    originalVideoClip.write_videofile(outputVideoName)
    
    print("Dubbed video written as", outputVideoName)
    
if __name__=="__main__":
    # Keep the input video name as input.mp4
    # Common Language code
    # Tamil: ta-IN
    # Hindi: hi
    # English:  en-IN
    apiKey = input("Enter your 11 labs api key: ")
    languageCode = input("Enter language code: ")
    print("Dubbing...")
    dubVideo("input.mp4", apiKey, "hi")