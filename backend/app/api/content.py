from fastapi import APIRouter, HTTPException
from app.services.llm_handler import generate_content
from app.services.image_gen import generate_image
from app.models.schemas import ContentRequest, ContentResponse

router = APIRouter()

@router.post("/", response_model=ContentResponse)
def create_content(request: ContentRequest):
    content = generate_content(request.topic, request.audience, request.platform, request.user_info, request.language)
    image_url = generate_image(request.topic)
    if not content:
        raise HTTPException(status_code=500, detail="Content generation failed")
    return ContentResponse(content=content, image_url=image_url)
