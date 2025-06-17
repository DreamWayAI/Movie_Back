from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import requests
from io import BytesIO

app = FastAPI()

D_ID_API_KEY = "your_did_api_key"

@app.post("/animate")
async def animate_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    headers = {"Authorization": f"Bearer {D_ID_API_KEY}"}
    response = requests.post(
        "https://api.d-id.com/talks", 
        headers=headers,
        files={"source_image": ("image.jpg", image_bytes, file.content_type)},
        data={"script": "Say hello from AI!"}
    )
    talk_response = response.json()
    video_url = talk_response.get("result_url")
    video_data = requests.get(video_url).content
    return StreamingResponse(BytesIO(video_data), media_type="video/mp4")