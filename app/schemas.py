from pydantic import BaseModel, EmailStr
from datetime import datetime

"""
Well technically, schemas are not actually necessary, 
but it is used to specify what exactly we want from the frontend
"""

# Users
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


# Posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool | None = True
    

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode: True


# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None