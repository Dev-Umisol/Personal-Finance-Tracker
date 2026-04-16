from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from app import models

def create_user(db: Session, username, password):
    password_hash = PasswordHash.recommended()
    hashed_password = password_hash.hash(password)

def get_user_by_username(db: Session, username):
    pass

def create_transactions(db: Session, user_id, item_name, item_description, amount):
    pass

def get_all_transactions(db: Session, user_id):
    pass

def delete_transactions(db: Session, id):
    pass