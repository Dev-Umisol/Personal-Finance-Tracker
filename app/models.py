from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from app.database import Base

class Transactions(Base):
    __tablename__ = "Transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    item_name = Column(String, nullable=True)
    
class Users(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)