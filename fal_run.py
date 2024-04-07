import os
import asyncio
import click
from dotenv import load_dotenv
import requests
# Assume fal_client and MODELS are properly imported from your setup
from scripts.fal import submit_request

from scripts.utils import store_video_from_response

load_dotenv()

IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")

def extract_first_url(response):
    """
    Extracts the first URL from the 'images' list within the provided response dictionary.

    Parameters:
    - response (dict): A dictionary containing at least an 'images' key with a list of image info dictionaries.

    Returns:
    - str: The URL of the first image or None if not found.
    """
    try:
        # Access the list of images and extract the URL of the first one
        return response['images'][0]['url']
    except (KeyError, IndexError):
        # Handle the case where 'images' key is not present or the list is empty
        return None
    
async def upload_image_to_imgur(image_bytes):
    """Simulated upload function. Replace with actual upload logic."""
    url = "https://api.imgur.com/3/image"
    headers = {
        "Authorization": f"Client-ID {IMGUR_CLIENT_ID}"
    }
    response = requests.post(url, headers=headers, files={'image': image_bytes})
    return response.json()["data"]["link"]

async def process_images_to_video(image_urls):
    """Takes image URLs, generates a video, and returns the video content or URL."""
    video_result = await submit_request(
        'images-to-video', image_url=image_urls[0])  # Simplified for one image
    return video_result

async def main(text_prompt):
    # Step 1: Generate images from text
    images_result = await submit_request(
        'text-to-images', prompt=text_prompt)
    img_url = extract_first_url(images_result)
    # Simulated response handling. Adjust based on actual `submit_request` response structure.
    # Step 3: Pass the image URLs to generate videos
    video_content = await process_images_to_video(img_url)
    store_video_from_response(video_content)
    # Step 4: Handle the video content
    # print(video_content)
    return video_content

@click.command()
@click.option('--text_prompt', prompt='Enter your text prompt', help='Text prompt for generating images.')
def run(text_prompt):
    asyncio.run(main(text_prompt))

if __name__ == "__main__":
    run()
