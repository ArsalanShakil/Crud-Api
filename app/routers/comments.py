from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import current_user

from ..schemas import posts
from .. import models, oauth2, database
from sqlalchemy.orm import Session


router =  APIRouter(
    prefix="/comment",
    tags= ['Comments']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comments(comment: posts.CommentOut, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {comment.post_id} does not exist")

    comment_query = db.query(models.Comments).filter(
        models.Comments.post_id == comment.post_id, models.Comments.user_id == current_user.id)

    found_vote = comment_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}