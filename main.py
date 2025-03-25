from fastapi import FastAPI
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


# starting the webserver
# uvicorn <file name without .py>:<fast api object name> in the terminal
# uvicorn main:app --reload


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    return {"message": "Hello World!!!!"}


@app.get("/posts")
def get_posts():
    return {"posts": "This is a post"}

@app.post("/createpost")
def create_post(pay_load: dict = Body(...)):
    print(pay_load)
    return {"message": "made a post"}