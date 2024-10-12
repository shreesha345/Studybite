import re
def timestampToSecond(ts: str):
    '''
    Converts a given timestamp of the format hh:mm:ss to total seconds
    '''
    hr, minn, sec = map(int, ts.split(":"))
    return 3600*hr + 60*minn + sec

def extractVideoIdFromUrl(videoUrl: str) -> str:
    # Matches the url of one of the type and return
    r = re.search(r"youtu.be/([\w\d-]+)|v=([\w\d-]+)|live/([\w\d-]+)", videoUrl).groups()
    return r[0] or r[1] or r[2]

def embed(ytVideoUrl: str, ts1: str = "00:00:00", ts2: str = "00:01:00") -> str:
    '''
    Returns an embeddable iframe html code of a yt video given ts1 and ts2 as start and end timestamps
    '''
    embeddingTemplate = '''
    <iframe width="560" height="315" src="https://www.youtube.com/embed/{}?start={}&end={}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    '''
    videoId = extractVideoIdFromUrl(ytVideoUrl)
    start = timestampToSecond(ts1)
    end = timestampToSecond(ts2)
    
    return embeddingTemplate.format(videoId, start, end)

def writeDemoHtml(iframe: str):
    '''
    Writes a demo html code to test the iframe embedding
    '''
    demoTemplate='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    Youtube video
    {}
</body>
</html>'''
    outputFileName = "embedTest.html"
    with open(outputFileName,"w") as f:
        f.write(demoTemplate.format(iframe))
    print(f"Demo code written in {outputFileName}")
    
url = input("Enter a youtube video url: ")
ts1 = input("Enter start timestamp in the format of hh:mm:ss ")
ts2 = input("Enter end timestamp in the format of hh:mm:ss ")
print("iframe embedding:\n")
embeddedCode = embed(url, ts1, ts2)
print(embeddedCode)
writeDemoHtml(embeddedCode)