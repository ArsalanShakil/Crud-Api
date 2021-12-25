from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import current_user

from ..schemas import comments
from .. import models, oauth2, database
from sqlalchemy.orm import Session


router =  APIRouter(
    prefix="/comment",
    tags= ['Comments']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comments(comment: comments.CommentCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {comment.post_id} does not exist")

    new_comment = models.Comments(**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment
