from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import current_user

from ..schemas import comments
from .. import models, oauth2, database
from sqlalchemy.orm import Session


router =  APIRouter(
    prefix="/comment",
    tags= ['Comments']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=comments.Comment)
def create_comments(comment: comments.CommentBase, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {comment.post_id} does not exist")

    new_comment = models.Comments(user_id=current_user.id,**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comments(id: int, db: Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user)):

    comment_query = db.query(models.Comments).filter(models.Comments.id == id)
    comment = comment_query.first()
    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"comment with id: {id} was not found")
        
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"not authorized to perform this action")
    
    comment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=comments.Comment)
async def update_comments(id: int,updated_comment: comments.CommentUpdate, db: Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user)):

    comment_query = db.query(models.Comments).filter(models.Comments.id == id)
     
    comment = comment_query.first()
    

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"comment with id: {id} was not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"not authorized to perform this action")
    
    comment_query.update(updated_comment.dict(),synchronize_session=False)
    
    db.commit()

    return comment_query.first()