from app.models.schemas import ContentRequest, ContentResponse
import openai
import requests
import os

def generate_content(request: ContentRequest) -> ContentResponse:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    prompt = f"Generate content for {request.platform} on the topic {request.topic} for {request.audience}"
    if request.personal_info:
        prompt += f" including details about {request.personal_info}"
    
    # Integrar Tavily para obtener imágenes relevantes
    tavily_response = requests.get(
        "https://api.tavily.com/search",
        params={"query": f"images for {request.topic}"},
        headers={"Authorization": f"Bearer {tavily_api_key}"}
    )
    image_url = tavily_response.json().get('results', [])[0].get('url', '') if tavily_response.json().get('results') else ''
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
        n=1,
        stop=None,
        language=request.language
    )
    
    return ContentResponse(content=response.choices[0].text, image_url=image_url)
