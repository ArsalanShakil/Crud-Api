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




@app.get("/")
async def root():
    return {"message": "Hello World!!"}



@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
        #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts



@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
        #              (post.title, post.content, post.published))
        #new_post = cursor.fetchone()
        #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post



@app.get("/posts/{id}", response_model=schemas.Post)
async def get_one_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
        # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
    return post




@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
        # deleted_post = cursor.fetchone()
        # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")    
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}", response_model=schemas.Post)
async def update_posts(id: int,updated_post: schemas.PostCreate, db: Session = Depends(get_db)):


    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        #                (post.title, post.content, post.published, str(id)))
        # updated_post = cursor.fetchone()
        # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
     
    post = post_query.first()
    

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    
    db.commit()

    return post_query.first()




@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
