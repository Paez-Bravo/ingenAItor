from fastapi import FastAPI
from app.api import content, auth, social
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.include_router(content.router, prefix="/content", tags=["content"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(social.router, prefix="/social", tags=["social"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the IngenIAtor content generation system!"}
