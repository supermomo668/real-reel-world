import asyncio
import click
import fal_client

from scripts.constants import FAL_MODELS as MODELS
async def submit_request(mode, **kwargs):
    model_details = MODELS.get(mode)
    if not model_details:
        print("Invalid mode selected.")
        return

    handler = await fal_client.submit_async(model_details['name'], arguments={key: kwargs[key] for key in model_details['args'] if key in kwargs})

    log_index = 0
    async for event in handler.iter_events(with_logs=True):
        if isinstance(event, fal_client.InProgress):
            new_logs = event.logs[log_index:]
            for log in new_logs:
                print(log["message"])
            log_index = len(event.logs)

    result = await handler.get()
    return result


@click.command()
@click.option('--mode', type=click.Choice(['text-to-images', 'images-to-video']), prompt=True, help='Choose operation mode')
@click.option('--prompt', default='', help='Text prompt for generating images')
@click.option('--negative_prompt', default='', help='Negative prompt to exclude certain elements in images')
@click.option('--image_size', default='square_hd', help='Size of the generated image')
@click.option('--num_inference_steps', default=25, help='Number of inference steps')
@click.option('--guidance_scale', default=7.5, help='Guidance scale for image generation')
@click.option('--num_images', default=1, help='Number of images to generate')
@click.option('--format', default='jpeg', help='Format of the generated images')
@click.option('--image_url', default='', help='URL of the image to use as a starting point for the video generation')
@click.option('--motion_bucket_id', default=127, help='Motion bucket id for video generation')
@click.option('--cond_aug', default=0.02, help='Conditioning augmentation for video generation')
@click.option('--steps', default=4, help='Number of steps for the model')
@click.option('--fps', default=10, help='FPS of the generated video')
def main(mode, prompt, negative_prompt, image_size, num_inference_steps, guidance_scale, num_images, format, image_url, motion_bucket_id, cond_aug, steps, fps):
    asyncio.run(submit_request(
      mode, 
      prompt=prompt, 
      negative_prompt=negative_prompt, 
      image_size=image_size, 
      num_inference_steps=num_inference_steps,
      guidance_scale=guidance_scale, 
      num_images=num_images, format=format, 
      image_url=image_url, 
      motion_bucket_id=motion_bucket_id, 
      cond_aug=cond_aug, steps=steps, fps=fps))

if __name__ == "__main__":
    main()