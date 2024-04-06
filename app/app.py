from fastapi import FastAPI, File, UploadFile
from typing import List
import boto3
from models import Video, create_video_metadata

app = FastAPI()

s3_client = boto3.client('s3', aws_access_key_id='YOUR_KEY', aws_secret_access_key='YOUR_SECRET')

@app.post("/upload-video/")
async def upload_video(title: str, tags: List[str], file: UploadFile = File(...)):
    # Upload video to S3
    s3_client.upload_fileobj(file.file, "your-bucket-name", file.filename)
    s3_url = f"https://your-bucket-name.s3.amazonaws.com/{file.filename}"
    
    # Save metadata in DB
    create_video_metadata(title, tags, s3_url)
    return {"url": s3_url}

@app.get("/videos/")
async def list_videos():
    # Query DB for videos
    videos = Video.query.all()  # Simplified; implement actual DB query
    return videos
