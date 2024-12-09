from openai import OpenAI

def generate_image(prompt: str) -> str:
    response = OpenAI.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

