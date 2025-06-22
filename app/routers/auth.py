from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["authentication"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # OAuth2PasswordRequestForm returns in a form of dictionary:
    # {
    #   "username": "...", --> email in our case
    #   "password": "..."
    # }

    # verifying if the user is actually registered or not by their email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # validating the password by hashing
    if not utils.verify_passwords(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # create a token
    # return the token
    access_token = oauth2.create_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer", "current_user": user.email}
