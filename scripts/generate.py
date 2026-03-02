import json
import sys
import os
import requests
from datetime import datetime


def generate_image(json_prompt_path, output_dir="images"):
    """Send a JSON prompt to Nano Banana 2 and save the result."""
    with open(json_prompt_path, 'r') as f:
        prompt_data = json.load(f)

    FAL_KEY = os.environ.get("FAL_KEY")

    payload = {
        "prompt": prompt_data["prompt"],
        "negative_prompt": prompt_data.get("negative_prompt", ""),
        "image_size": prompt_data.get("settings", {}).get("resolution", "1024x1024"),
    }

    response = requests.post(
        "https://fal.run/fal-ai/nano-banana-2",
        headers={
            "Authorization": f"Key {FAL_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    result = response.json()
    image_url = result["images"][0]["url"]
    img_data = requests.get(image_url).content

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{timestamp}.png"
    os.makedirs(output_dir, exist_ok=True)

    with open(filename, 'wb') as f:
        f.write(img_data)

    print(f"Image saved: {filename}")
    return filename


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py <path-to-json-prompt>")
        sys.exit(1)

    generate_image(sys.argv[1])
