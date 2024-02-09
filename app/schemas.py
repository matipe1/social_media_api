from pydantic import BaseModel, EmailStr
from datetime import datetime

"""
Well technically, schemas are not actually necessary, 
but it is used to specify what exactly we want from the frontend
"""

class PostBase(BaseModel):
    title: str
    content: str
    published: bool | None = True
    

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode: True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode: True


class UserLogin(BaseModel):
    email: EmailStr
    password: str