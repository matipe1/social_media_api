from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine

from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


app.include_router(post.router)
app.include_router(user.router)

@app.get('/')
def greetings():
    return {"status": "API is running..."}