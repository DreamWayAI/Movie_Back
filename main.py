from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests
import os
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "vk-3bHcHfaAlflBADMAKGG3BtiDqvIxMSfDQMJT0VNkAnXyU"

@app.post("/generate")
async def generate(file: UploadFile = File(...), prompt: str = Form(...)):
    files = {
        "file": (file.filename, await file.read(), file.content_type)
    }
    data = {
        "prompt": prompt,
        "aspect_ratio": "square",
        "motion": "default"
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    init_res = requests.post("https://api.pika.art/v1/gen", headers=headers, files=files, data=data)
    job_id = init_res.json().get("id")

    # Очікуємо завершення генерації
    for _ in range(30):
        time.sleep(5)
        status_res = requests.get(f"https://api.pika.art/v1/gen/{job_id}", headers=headers)
        data = status_res.json()
        if data.get("status") == "succeeded":
            video_url = data.get("video_url")
            video = requests.get(video_url)
            return StreamingResponse(iter([video.content]), media_type="video/mp4")

    return {"error": "Timed out"}