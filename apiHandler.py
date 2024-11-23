from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from dub import dubVideo
import os

templates =  Jinja2Templates(directory="templates")

app = FastAPI(debug=True)

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/upload")
def upload_video(video: UploadFile = File(...),
                   api_key: str = Form(...), 
                   target_lang: str = Form(...)):
    with open(video.filename, "wb") as f:
        f.write(video.file.read())
    dubVideo(video.filename, api_key, target_lang)
    return "Video saved as output.mp4"