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
from . import models, schemas

models.Base.metadata.create_all(bind=engine)
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

# default path
@app.get("/")
async def root():
    return {"message": "Hello, welcome to my api"}


# gets all posts
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # posts = cursor.execute("""SELECT * FROM fastapi_posts""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return posts


# creates a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO fastapi_posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()

    new_post = models.Post(**post.dict())  # this will unpack the dictionary for us
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# retrieves a single post given a id
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM fastapi_posts WHERE id=%s""", (str(id)))
    # retrieved_post = cursor.fetchone()
    retrieved_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not retrieved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} was found")
    return retrieved_post


# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM fastapi_posts WHERE id=%s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    post = db.query(models.Post).filter(models.Post.id == id)  # saving it as a query

    if post.first() is None:  # run the query and check if it exists
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    # if post does exist
    post.delete(synchronize_session=False)  # this is to prevent any stale entries from update or delete to
    # linger around until the session ends (after committing)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating a post
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE fastapi_posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


"""
User focused functions/paths
"""


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
