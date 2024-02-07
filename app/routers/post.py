



@app.get('/')
def greetings():
    return {"status": "API is running..."}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING *; """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()

    new_post = models.Post(**dict(post)) # title=post.title, content=post.content, published=post.published

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get('/posts', response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts; """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts



@app.get('/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post


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




@app.put('/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
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

    return new_post