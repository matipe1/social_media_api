from pydantic import BaseModel
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