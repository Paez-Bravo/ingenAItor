from fastapi import APIRouter, Depends
from app.services.llm_handler import generate_content
from app.models.schemas import ContentRequest, ContentResponse

router = APIRouter()

@router.post("/", response_model=ContentResponse)
def create_content(request: ContentRequest):
    content = generate_content(request)
    return content
