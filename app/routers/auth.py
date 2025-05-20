from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session
from .. import database

router = APIRouter(
    tags=["authentication"]
)

@router.post("/login")
def login(db: Session = Depends(database.get_db)):

