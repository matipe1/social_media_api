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
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING *; """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()

    new_post = models.Post(**dict(post)) # title=post.title, content=post.content, published=post.published

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"msg": "New post created",
            "data": new_post}


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts; """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return {"data": posts}



@app.get('/posts/{id}', status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return {"data": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *; """, (str(id),))
    # deleted_post = cursor.fetchone()
    # connection.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post.delete(synchronize_session=False)
    db.commit()




@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id = %s RETURNING *; """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    new_post = post_query.first()

    if new_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post_query.update(dict(post), synchronize_session=False)
    db.commit()

    return {"msg": f"Post with id {id} updated", "data": new_post}