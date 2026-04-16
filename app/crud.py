from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from app import models

# Create a new user with hashed password and store in the database
def create_user(db: Session, user_name: str, password: str) -> models.Users:
    password_hash = PasswordHash.recommended()
    hashed_password = password_hash.hash(password)
    
    db_user = models.Users(user_name = user_name, user_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Retrieve a user from the database by their username
def get_user_by_username(db: Session, user_name: str) -> models.Users | None:
    return db.query(models.Users).filter(models.Users.user_name == user_name).first()

# Create a new transaction and store it in the database
def create_transactions(db: Session, user_id: int, item_name: str, item_description: str, amount: float) -> models.Transactions:
    db_transactions = models.Transactions(user_id = user_id, item_name = item_name, item_description = item_description, amount = amount)
    
    db.add(db_transactions)
    db.commit()
    db.refresh(db_transactions)
    
    return db_transactions

# Retrieve a transaction from the database by user_id
def get_all_transactions(db: Session, user_id: int) -> models.Transactions | list:
    return db.query(models.Transactions).filter(models.Transactions.user_id == user_id).all()

# Retrieve item id from the database and delete
def delete_transactions(db: Session, id: int):
    pass