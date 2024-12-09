from fastapi import APIRouter, HTTPException
from app.services.financial_api import get_financial_news

router = APIRouter()

@router.get("/financial", response_model=list)
async def get_financial_news_endpoint():
    try:
        news = get_financial_news()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return news
