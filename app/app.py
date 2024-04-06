# from fastapi import FastAPI, File, UploadFile
from typing import List
import boto3
# from models import Video, create_video_metadata
from botocore.exceptions import ClientError
import os
from loguru import logger

class AWSClient:

    def __init__(self):
        self.boto3 = boto3.client('s3', aws_access_key_id=os.environ['ACCESS_KEY_ID'], aws_secret_access_key=os.environ['SECRET_ACESS_KEY'])
        self.bucket_name = "poehack"

    def upload_video(self, file_name, object_name=None) -> bool:
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        try:
            response = self.boto3.upload_file(file_name, self.bucket_name, object_name)
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def download_video(self, file_name)->str:
        download_path = "demo_videos/new_download.mp4"
        self.boto3.download_file(Bucket = self.bucket_name, Filename = download_path, Key=file_name)
        return download_path

if __name__ == "__main__":
    # await upload_video(title, tags)
    # upload_file("demo_videos/sample_video.mp4 (240p).mp4", "poehack", "1.mp4")
    boto3_client = AWSClient()
    boto3_client.download_video("sample_video.mp4 (240p).mp4")


# @app.get("/videos/")
# async def list_videos():
#     # Query DB for videos
#     videos = Video.query.all()  # Simplified; implement actual DB query
#     return videos

# app = FastAPI()

# s3_client = boto3.client('s3', aws_access_key_id=os.environ['ACCESS_KEY_ID'], aws_secret_access_key=os.environ['SECRET_ACESS_KEY'])

# @app.post("/upload-video/")
# async def upload_video(title: str, tags: List[str], file: UploadFile = File(...)):
#     # Upload video to S3
#     s3_client.upload_fileobj(file.file, "poehack", file.filename)
#     s3_url = f"https://poehack.s3.amazonaws.com/{file.filename}"
    
#     # Save metadata in DB
#     create_video_metadata(title, tags, s3_url)
#     return {"url": s3_url}
