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



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int, db: Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user)):

    comment_query = db.query(models.Comments).filter(models.Comments.id == id)
    comment = comment_query.first()
    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"comment with id: {id} was not found")
        
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"not authorized to perform this action")
    
    comment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# @router.put("/{id}", response_model=posts.Post)
# async def update_posts(id: int,updated_post: posts.PostCreate, db: Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user)):

#     post_query = db.query(models.Post).filter(models.Post.id == id)
     
#     post = post_query.first()
    

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
#     if post.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"not authorized to perform this action")
    
#     post_query.update(updated_post.dict(),synchronize_session=False)
    
#     db.commit()

#     return post_query.first()