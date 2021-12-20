from typing import Optional, List
from fastapi import FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

    
while True:
        try:  
            conn = psycopg2.connect(host = '' ,database = '',
                                    user = '',password = '',cursor_factory = RealDictCursor)
            cursor = conn.cursor()
            print("DB connected!!!")
            break
        except Exception as error:
            print("DB connection failed")
            print("Error", error)
            time.sleep(2)
    

my_post = [{"title": "title post 1","content": "content post 1", "id": 1},{"title": "food","content": "pizza", "id": 2}]


def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
async def root():
    return {"message": "Hello World!!"}