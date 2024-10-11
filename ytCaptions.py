from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from deep_translator import GoogleTranslator
import concurrent.futures
import re

# Hindi to english translator
transEngine = GoogleTranslator(source="hi", target="en")

def secondsToTimestamp(s: int) -> str:
    '''
    Convert seconds to timestamp with mm:ss format
    '''
    
    minutes, remainingSeconds = divmod(round(s), 60)
    return f"{minutes}:{remainingSeconds}"

def translateTrans(d: dict) -> dict:
    return {
        "start":secondsToTimestamp(d["start"]),
        "end":secondsToTimestamp(d["start"] + d["duration"]),
        "text":transEngine.translate(d["text"])
    }

def extractVideoIdFromUrl(videoUrl: str) -> str:
    # Matches the url of one of the type and return
    r = re.search(r"youtu.be/([\w\d-]+)|v=([\w\d-]+)", videoUrl).groups()
    return r[0] or r[1]
    
def getCaptions(youtubeVideoUrl: str) -> dict | str:
    '''
    Returns dictionary of start, end and each caption of the video
    '''
    videoId = extractVideoIdFromUrl(youtubeVideoUrl)
    try:
        # Tries to find english transcription and collect it
        trans = YouTubeTranscriptApi.list_transcripts(videoId).find_transcript(["en"])
        
        # Parse each dicts and return
        return [
                {
            "start":secondsToTimestamp(d["start"]),
            "end":secondsToTimestamp(d["start"] + d["duration"]),
            "text":d["text"]
            }
            for d in trans.fetch()
        ]
    
    except TranscriptsDisabled:
        # If transcription is disabled for the video
        return "Transcripts disabled for the video"
    
    except NoTranscriptFound:
        # If english transcription is not found then it finds for the hindi transcription and collects it
        trans = YouTubeTranscriptApi.list_transcripts(videoId).find_transcript(["hi"])
        
        # Translating each dicts of transcription with threading to speed up the process
        with concurrent.futures.ThreadPoolExecutor() as exe:
            parsedTrans = exe.map(translateTrans, trans.fetch())
            return list(parsedTrans)
    except:
        # If an unknown error occurs
        return "Cannot fetch transcription for this video"

url = input("Enter a yt video link: ")
print()
print(getCaptions(url))