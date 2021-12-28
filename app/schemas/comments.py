from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

from app.database import Base



class CommentBase(BaseModel):
    post_id:int
    content:str 
    
class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    user_id:int
    class Config:
        orm_mode = True   

class CommentOut(BaseModel):
    Comment: Comment
    class Config:
        orm_mode = True
        
class CommentUpdate(BaseModel):
    content:str 