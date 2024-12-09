from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils.token_manager import create_access_token, verify_password, decode_access_token
from app.models.schemas import Token, User
from app.db.sqlite import get_db_connection
from app.db.mongodb import get_db
import sqlite3

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(username: str):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

@router.get("/users/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user(payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
