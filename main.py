from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from random import randrange

app = FastAPI()


# Schema validation with Pydantic library (using BaseModel)
class Post(BaseModel):
    title: str
    content: str
    published: bool | None = False
    rating: int | None = None


# Database
my_fake_db = [
    {
        "id": 1,
        "title": "The power of Positive Thinking",
        "content": "You have to read this amazing book",
        "published": True,
        "rating": 5
    },
    {
        "id": 2,
        "title": "Atomic Habits",
        "content": "How tiny habits could change your life in the long term",
        "published": False,
        "rating": 5
    }
]


# Functions
def find_post(id):
    for post in my_fake_db:
        if post['id'] == id:
            return post
    return -1


def find_index_post(id):
    for index, post in enumerate(my_fake_db):
        if post['id'] == id:
            return index


# API
@app.get('/')
def greetings():
    return {"status": "API is running..."}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post): # Specify the schema you want to receive into a variable
    
    post_dict = dict(new_post)
    id = randrange(0, 100000000)

    while find_post(id) != -1:
        id = randrange(0, 100000000)
    post_dict['id'] = id
    my_fake_db.append(post_dict)

    return {"msg": "New post created",
            "data": Post(**post_dict)}


@app.get('/posts')
def get_posts():
    return {"data": my_fake_db}


@app.get('/posts/{id}', status_code=status.HTTP_200_OK)
def get_post(id: int):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return {"data": post}


# It's the reason because order matters -> API will consider this path as: /posts/{id}
# @app.get('/posts/latest')
# def get_latest_post():
#     post = my_fake_db[len(my_fake_db) - 1]
#     return {"data": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    my_fake_db.pop(index)
