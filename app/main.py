from random import randrange
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

# directory imports
from .database import engine, get_db
from . import models, schemas, utils
from .routers import posts, users, auth



models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# TODO: keep adding JWT oauth2 token
"""

"""

"""
Bottom three lines of code are: path operations (FastAPI documentation) or route (other documentations)

Two components:
    1) Decorator:
        - app = reference to the object
        - get = type of request
        - "/" = path after domain

    2) Function:
        - regular python function
        - 'async' keyword only needed when performing a asynchronous task, like calling a api, or talking to db
            otherwise, it's optional
        - root is just a name, it can be anything, but keep them descriptive (remember C chat server?)

Starting the webserver

    uvicorn <file name without .py>:<fast api object name> in the terminal
    uvicorn main:app --reload
"""

while True:
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password=utils.verify_env("PASSWORD"),
            cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(2)

# my_posts = [
#     {
#         "title": "post 1 title",
#         "content": "post 1 content",
#         "id": 1
#     },
#     {
#         "title": "cotton candy",
#         "content": "condy content",
#         "id": 2
#     }
# ]

"""
Database name:  fastapi
Table name:     fastapi_posts
"""

"""
A view of how ORM differs from regular SQL in python code:

@app.get("/sql")
def test_posts(db: Session = Depends(get_deb)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# gets all posts
@app.get("/posts")
def get_posts():
    posts = cursor.execute(\"""SELECT * FROM fastapi_posts\""")
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}
"""


# TODO: Add user functionalities (i.e. create account, login, make post, etc)

# routing paths
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


# default path
@app.get("/")
async def root():
    return {"message": "Hello, welcome to my api"}
