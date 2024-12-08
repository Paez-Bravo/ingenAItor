from fastapi import APIRouter, Depends
from app.services.scheduler import schedule_post
from app.models.schemas import PostRequest, PostResponse

router = APIRouter()

@router.post("/schedule", response_model=PostResponse)
def schedule_social_post(request: PostRequest):
    post = schedule_post(request)
    return post
