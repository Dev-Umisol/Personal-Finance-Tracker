from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Schemas for User and Transaction models
class UserCreate(BaseModel):
    user_name: str
    user_password: str

# Response schema for User model
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # This allows the model to be created from an ORM object, which is useful when returning data from the database.
    
    id: int
    user_name: str

# Schemas for Transaction model
class TransactionCreate(BaseModel):
    item_name: str
    amount: float
    item_description: str

# Response schema for Transaction model
class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # This allows the model to be created from an ORM object, which is useful when returning data from the database.
    
    id: int
    user_id: int
    item_name: str
    amount: float
    item_description: str
    created_at: datetime

# Request schema for user login / same as UserCreate but can be separated for clarity / used later for refactoring or adding additional fields specific to login if needed
class UserLogin(BaseModel):
    user_name: str
    user_password: str