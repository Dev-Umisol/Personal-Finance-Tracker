import jwt
import os

from dotenv import load_dotenv
from app.main import create_access_token

# Key Configuration
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if SECRET_KEY is None:
    raise ValueError("SECRET_KEY environment variable is not set.")

# Test with a valid username
def test_create_access_token():
    username = "testuser"
    token = create_access_token(username)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert decoded_token["sub"] == username
    assert decoded_token["action"] == "login"
    assert "exp" in decoded_token

# Test with an empty username
def test_create_access_token_empty_username():
    username = ""
    token = create_access_token(username)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert decoded_token["sub"] == username
    assert decoded_token["action"] == "login"
    assert "exp" in decoded_token
    