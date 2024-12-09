import requests
import os

def post_to_instagram(content: str, platform: str):
    instagram_api_url = "https://graph.instagram.com/v12.0/me/media"
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    
    payload = {
        "caption": content,
        "access_token": access_token
    }
    
    response = requests.post(instagram_api_url, data=payload)
    if response.status_code != 200:
        raise Exception("Failed to post to Instagram")
    return response.json()
