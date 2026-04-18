from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app import crud, schemas, models
from app.database import get_db, engine
from dotenv import load_dotenv

import jwt
import os

# Key Configuration
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if SECRET_KEY is None:
    raise ValueError("SECRET_KEY environment variable is not set.")

app = FastAPI(title="Personal Finance Tracker")

# Checks if table exists
models.Base.metadata.create_all(bind=engine)

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Generate a JWT access token for a logged-in user
# includes subject, login action, and expiration time
def create_access_token(user_name):
    payload = {
        "action": "login",
        "sub": user_name,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

