from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

# Define the Transactions model with a foreign key to the Users model
class Transactions(Base):
    __tablename__ = "Transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    item_name = Column(String, nullable=True)
    
    # Establish a relationship between Transactions and Users
    user = relationship("Users", back_populates="transactions")

# Define the Users model
class Users(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    
    # Establish a relationship between Users and Transactions
    transactions = relationship("Transactions", back_populates="user") 