import requests
from pathlib import Path
from datetime import datetime

from sqlalchemy import exists

def store_video_from_response(
  api_response, local_file_path=Path('assets')):
    # Extract video URL and file name from the response
    video_url = api_response.get("video", {}).get("url")
    file_name = api_response.get("video", {}).get("file_name")
    
    # Check if the URL and file name are present
    if not video_url or not file_name:
        print("Invalid API response: URL or file name missing.")
        return
    
    # Generate a unique file path by appending the current datetime
    datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_file_path = local_file_path/f"{local_file_path}_{datetime_str}_{file_name}.mp4"
    
    # Download the video file
    response = requests.get(video_url)
    if response.status_code == 200:
        # Ensure the directory exists
        local_file_path.mkdir(exist_ok=True)
        
        # Write the file to the specified path
        with open(unique_file_path, "wb") as file:
            file.write(response.content)
        print(f"File saved as {unique_file_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

if __name__=="__main__":
  # Example usage
  video_info = {
    "video": {
      "url": "https://example.com/path/to/video.png",
      "content_type": "image/png",
      "file_name": "z9RV14K95DvU.png",
      "file_size": 4404019
    }
  }

  store_video_from_response()(video_info['video']['url'], '/path/to/save/z9RV14K95DvU.png')
