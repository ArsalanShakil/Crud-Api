from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

from app.database import Base
from .users import UserOut

    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass

        
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int 
    owner: UserOut

    class Config:
        orm_mode = True
 
   
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
 
         
class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)
    
    
class CommentBase(BaseModel):
    post_id:int
    user_id:int
    content:str 

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    class Config:
        orm_mode = True   

class CommentOut(BaseModel):
    Comment: Comment
    class Config:
        orm_mode = True
        
