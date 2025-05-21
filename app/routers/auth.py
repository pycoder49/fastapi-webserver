from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils

router = APIRouter(tags=["authentication"])


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    # verifying if the user is actually registered or not by their email
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    # validating the password by hashing
    if not utils.verify_passwords(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    # create a token
    # return the token
    return {"token": "some token"}
