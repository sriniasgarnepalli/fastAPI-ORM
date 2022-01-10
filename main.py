from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

'''
Session local is kind of responsible for talking with the databases 
The function get_db() is created to get a connection to the database or get a session to the database.
Everytime we get a request we get a session to send SQL statements to the database after request is done we close the session
'''

# Dependency


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


class Post(BaseModel):
    title: str
    content: str
    number: str


# connecting to database and handling connection if connection fails
while True:

    try:
        conn = psycopg2.connect(host='enterHostName', database='EnterDBName', user='EnteruserName',
                                password='EnterPassword', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error : ", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1",
             "content": "content of post1", "number": "number of user", "id": 1}, {"title": "Favorite Actore", "content": "I am a die hard fan of RamCharan", "number": 1234567890, "id": 2}]


def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts}


@app.get("/posts")
async def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):
    post.dict()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return {"data": new_post}



@app.get('/posts/{id}')
def get_post(id=int, db: Session = Depends(get_db)):
    get_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f"Post with id: {id} was not found"}
    return {"post_details": get_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id=int, db: Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesnot exist")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    update_query = db.query(models.Post).filter(models.Post.id == id)
    post = update_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesnot exist")
    update_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {'data': update_query.first()}
