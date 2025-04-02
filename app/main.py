from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

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


# defining a schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='aryan',
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


# default path
@app.get("/")
async def root():
    return {"message": "Hello, welcome to my api"}


# gets all posts
@app.get("/posts")
def get_posts():
    posts = cursor.execute("""SELECT * FROM fastapi_posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}


# creates a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO fastapi_posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()
    print(new_post)
    return {"data": new_post}


# retrieves a single post given a id
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM fastapi_posts WHERE id=%s""", (str(id)))
    retrieved_post = cursor.fetchone()
    if not retrieved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} was found")
    return {"post": retrieved_post}


# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM fastapi_posts WHERE id=%s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    connection.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return {"Deleted post": deleted_post}


# updating a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")
