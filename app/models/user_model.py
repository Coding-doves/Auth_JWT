from typing import Union
from pydantic import BaseModel, EmailStr
from  datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str


class User(UserBase): # Responses
    is_active: bool
    created_date: Union[None, datetime] = None
    
    class Config:
        from_attribute=True
        arbitrary_types_allowed=True # Allow datetime format
