from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from io import BytesIO
import os

app = FastAPI()

# Додаємо CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/animate")
async def animate_image(file: UploadFile = File(...)):
    api_key = os.getenv("D_ID_API_KEY")
    if not api_key:
        return {"error": "Missing D_ID_API_KEY"}

    image_bytes = await file.read()

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "script": "Hello, this is your AI animation!",
        "driver_url": "bank://lively"
    }

    files = {
        "source_image": ("image.jpg", image_bytes, file.content_type)
    }

    response = requests.post(
        "https://api.d-id.com/talks",
        headers=headers,
        files=files,
        data=data
    )

    if response.status_code != 200:
        return {"error": "Failed to create animation", "details": response.text}

    result = response.json()
    video_url = result.get("result_url")
    if not video_url:
        return {"error": "No result_url in response"}

    video_data = requests.get(video_url).content
    return StreamingResponse(BytesIO(video_data), media_type="video/mp4")