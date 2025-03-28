from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

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
    rating: Optional[int] = None


my_posts = [
    {
        "title": "post 1 title",
        "content": "post 1 content",
        "id": 1
    },
    {
        "title": "cotton candy",
        "content": "condy content",
        "id": 2
    }
]


@app.get("/")
async def root():
    return {"message": "Hello, welcome to my api"}


# gets all posts
@app.get("/posts")
def get_posts():
    return {"posts": my_posts}


# creates a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    print(post_dict)
    my_posts.append(post_dict)
    return {"data": my_posts}


# retrieves a single post given a id
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    for post in my_posts:
        if post["id"] == id:
            return {"post": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")


# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            del my_posts[i]
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")


# updating a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    for i, entry in enumerate(my_posts):
        if entry["id"] == id:
            post_dict = post.dict()
            post_dict["id"] = id
            my_posts[i] = post_dict
            return {"message": "updated post"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")
