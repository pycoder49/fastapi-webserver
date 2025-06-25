from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import and_
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    # first query to see if the vote already exists or not
    vote_query = db.query(models.Vote).filter(
        and_(
            models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user.id
        )
    )
    found_vote = vote_query.first()

    if vote.dir == 1:  # user already liked the post and will be prohibited from doing so again
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on this post (pid: {vote.post_id})")

        # adding the entry to the database if the vote does not exist
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}
    else:
        if not found_vote:  # user is trying to delete a vote that doesn't exist
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        # deleting from the table if the vote does exist
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
