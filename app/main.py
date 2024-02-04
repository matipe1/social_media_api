from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Schema validation with Pydantic library (using BaseModel)
class Post(BaseModel):
    title: str
    content: str
    published: bool | None = False
    # rating: int | None = None


while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                      password='password123', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print('Database connection was succesfull!')
        break

    except Exception as error:
        print('Connecting database failed')
        print(f'Error: {error}')
        time.sleep(2)


# API
@app.get('/')
def greetings():
    return {"status": "API is running..."}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post): # Specify the schema you want to receive into a variable
    cursor.execute("""INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING *; """, # This way to add the variables don't make you vulnerable to SQL Injection
                   (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()

    connection.commit()

    return {"msg": "New post created",
            "data": new_post}


@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts; """)
    posts = cursor.fetchall()

    return {"data": posts}


@app.get('/posts/{id}', status_code=status.HTTP_200_OK)
def get_post(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return {"data": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *; """, (str(id),))
    deleted_post = cursor.fetchone()
    connection.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id = %s RETURNING *; """,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()

    connection.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    

    return {"msg": f"Post with id {id} updated",
            "data": updated_post}