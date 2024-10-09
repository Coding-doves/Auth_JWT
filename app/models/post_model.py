from pydantic import BaseModel, EmailStr
from  datetime import datetime


class PostSchema(BaseModel):
    id: int = None
    title: str
    content: str

    class Config:
        from_attribute=True
