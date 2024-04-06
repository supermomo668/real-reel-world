import os
import click
import requests
import json 

from dotenv import load_dotenv
from scripts.constants import BRAVE_ENDPOINTS as ENDPOINTS
from datetime import datetime 


# Load environment variables from .env file
load_dotenv()

# API headers
HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "X-Subscription-Token": os.getenv("BRAVE_API_KEY")
}
prompt="corporate policy in the world that create the most lucrative busiunuess opportunity?"

def search(query=prompt, endpoint="news"):
    """Perform a search query using the selected Brave Search API endpoint."""
    api_url = ENDPOINTS[endpoint]['url']
    params = {'q': query}
    response = requests.get(
        api_url, headers=HEADERS, params=params)

    # Check if the request was successful
    if response.ok:
        return response.json()
    else:
        return {}

@click.command()
@click.argument('query', default="what is the second highest mountain?")
@click.option('--endpoint', type=click.Choice(['news', 'videos', 'images', 'web'], case_sensitive=False), default='news', help='Select the search endpoint.')
def main(query, endpoint):
    json_response = search(query, endpoint)
    # Ensure the 'assets' folder exists
    assets_dir = 'assets'
    os.makedirs(assets_dir, exist_ok=True)

    # Generate a unique filename based on the endpoint
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"search_result_{timestamp}.json"
    filepath = os.path.join(assets_dir, filename)

    # Write the JSON response to the file
    with open(filepath, 'w') as json_file:
        json.dump(json_response, json_file, indent=4)

    click.echo(f"Results saved to {filepath}")
    
if __name__ == "__main__":
    main()