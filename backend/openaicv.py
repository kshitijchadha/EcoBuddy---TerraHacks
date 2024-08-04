import base64
import requests
from dotenv import load_dotenv
import os 

load_dotenv()

# OpenAI API Key
api_key = os.getenv("API_KEY")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')  

def get_image_data(image_path):

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = "Find the main focus item of the image. Does the item go in the trash, recycling, or compost? RESPOND WITH: <ITEM NAME>: TRASH, RECYCLE, COMPOST. RESPOND WITH: NONE if you cant find the focus"

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)   
    return response.json()['choices'][0]['message']['content']

