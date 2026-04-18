from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
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

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Dependency function to authenticate and retrieve the current user from JWT token
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired Token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_name = decoded_token.get("sub")
    
    if user_name is None:
        raise HTTPException(status_code=401, detail="Invalid token: missing sub claim")
    
    fetch_user = crud.get_user_by_username(db, user_name)
    
    if fetch_user is None:
        raise HTTPException(status_code=401, detail="Invalid user")
    return fetch_user

# Register a new user with username and password
@app.post('/users/register', response_model=schemas.UserResponse, status_code=201)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.user_name):
        raise HTTPException(status_code=409, detail="Username already exists")
    else:
        new_user = crud.create_user(db, user.user_name, user.user_password)
        
    return new_user

# Endpoint for user login: authenticates user credentials and returns an access token
@app.post('/users/login')
def user_login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    password_hash = PasswordHash.recommended()
    password = crud.get_user_by_username(db, user.user_name)
    
    if password is None:
        raise HTTPException(status_code=401, detail="Username not found")
    
    is_valid = password_hash.verify(user.user_password, password.user_password) # type: ignore
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Password is not valid")
    
    return {
        "access_token": create_access_token(user.user_name),
        "token_type": "bearer"
    }