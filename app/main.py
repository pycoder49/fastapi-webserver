from fastapi import FastAPI
from .database import engine
from . import models
from .routers import posts, users, auth, vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware      # to allow requests from other domains


# models.Base.metadata.create_all(bind=engine)  --> Don't need this anymore because of alembic migrations
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

print(settings.algorithm)

# TODO:

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
    
    With package: uvicorn app.main:app --reload
"""

"""
A view of how ORM differs from regular SQL in python code:

@app.get("/sql")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
def get_posts():
    posts = cursor.execute(\"""SELECT * FROM fastapi_posts\""")
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}
"""

# routing paths
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


# default path
@app.get("/")
async def root():
    return {"message": "Hello, welcome to my api"}
