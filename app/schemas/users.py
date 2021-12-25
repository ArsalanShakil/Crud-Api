from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

from app.database import Base



class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime 

    class Config:
        orm_mode = True
        
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None