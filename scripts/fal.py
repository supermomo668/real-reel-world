import asyncio
import os
import click
import fal_client
from dotenv import load_dotenv

from .constants import FAL_MODELS as MODELS

# Load the environment variables
load_dotenv()

# Define the Click command
@click.command()
@click.option('--image-url', prompt='Image URL', help='URL of the image to process.')
@click.option('--prompt', prompt='Description prompt', help='Description of the desired transformation.')
def cli(image_url, prompt):
    asyncio.run(submit(image_url, prompt))
import asyncio
import os
import click
import fal_client
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


@click.group()
def cli():
    pass

@cli.command()
def list_models():
    """List available models and their descriptions."""
    for model_key, model_value in MODELS.items():
        click.echo(f"Model: {model_key}")
        click.echo(f"Name: {model_value['name']}")
        click.echo(f"Description: {model_value['description']}\n")

# Define the Click command
@click.command()
@click.argument('model_type', type=click.Choice(['image-to-image', 'fast-svd'], case_sensitive=False))
@click.option('--image-url', prompt='Image URL', help='URL of the image to process.')
@click.option('--prompt', default='', help='Description of the desired transformation (only for image-to-image).')
def cli(model_type, image_url, prompt):
    asyncio.run(submit(model_type, image_url, prompt))

async def submit(model_type, image_url, prompt):
    if model_type == 'image-to-image':
        arguments = {
            "image_url": image_url,
            "prompt": prompt
        }
        model_name = "fal-ai/fast-sdxl/image-to-image"
    elif model_type == 'fast-svd':
        arguments = {
            "image_url": image_url
        }
        model_name = "fal-ai/fast-svd"

    handler = await fal_client.submit_async(model_name, arguments=arguments)

    log_index = 0
    async for event in handler.iter_events(with_logs=True):
        if isinstance(event, fal_client.InProgress):
            new_logs = event.logs[log_index:]
            for log in new_logs:
                print(log["message"])
            log_index = len(event.logs)

    result = await handler.get()
    print(result)


if __name__ == '__main__':
  # python cli_submit.py list-models
  cli()