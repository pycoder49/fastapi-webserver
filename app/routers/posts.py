from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# gets all posts -- don't need "/posts" because of prefix was set above
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10,      # for limiting the amount the posts returned
              skip: int = 0,        # for skipping (or offsetting) an amount of psots
              search: Optional[str] = ""):
    # posts = cursor.execute("""SELECT * FROM fastapi_posts""")
    # posts = cursor.fetchall()
    # print(posts)

    # limit here is a query parameter, and you can send it by adding a "?" at the end of the endpoint
    # /posts?limit=3
    # .offset(int) is for skipping the number of posts
    query = db.query(models.Post)

    if search:
        query = query.filter(models.Post.title.contains(search))

    return query.limit(limit).offset(skip).all()


# creates a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO fastapi_posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()

    print(current_user.id)

    # this will unpack the dictionary for us.
    # The user should not have to pass in the
    # user id when creating a post (This takes the
    # current user and uses that id
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# retrieves a single post given a id
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int,
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM fastapi_posts WHERE id=%s""", (str(id)))
    # retrieved_post = cursor.fetchone()
    retrieved_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not retrieved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} was found")
    return retrieved_post


# deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM fastapi_posts WHERE id=%s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)  # saving it as a query
    post = post_query.first()

    # checking the user is deleting his own post or someone else's
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You're not the owner of this post")

    if post is None:  # run the query and check if it exists
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    # if post does exist
    post_query.delete(synchronize_session=False)  # this is to prevent any stale entries from update or delete to
    # linger around until the session ends (after committing)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating a post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int,
                updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE fastapi_posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # checking the user is deleting his own post or someone else's
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You're not the owner of this post")

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
