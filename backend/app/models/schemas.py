from pydantic import BaseModel

class ContentRequest(BaseModel):
    topic: str
    audience: str
    platform: str
    personal_info: str = None
    language: str = "en"

class ContentResponse(BaseModel):
    content: str
    image_url: str = None

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    hashed_password: str

class PostRequest(BaseModel):
    content: str
    platform: str
    schedule_time: str

class PostResponse(BaseModel):
    status: str
    scheduled_time: str
