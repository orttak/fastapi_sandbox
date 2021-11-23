#source >>> https://testdriven.io/blog/fastapi-crud/#get-routes
#activate venv source activate fastapi
from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange
from typing import Optional, List

#below line go to utils.py
#from passlib.context import CryptContext
#import db driver
import psycopg2
from psycopg2.extras import RealDictCursor

from  sqlalchemy.orm import Session

from . import models, schemas,utils
from app.database import  engine ,get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI()



@app.get("/")
def root():
    return {"message":"Hello world"}

try:
    #if you work with docker compose, host name should db name from docker-compose.yml
    conn = psycopg2.connect(dbname="hello_fastapi_dev", user="hello_fastapi", password="hello_fastapi", host="db", port="5432",\
        cursor_factory=RealDictCursor)
    cursor=conn.cursor()
except Exception as error:
    print("Error while connecting to the database")
    print(f"Error is {error}")

@app.get('/posts',response_model=List[schemas.PostResponse])
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts=cursor.fetchall()
    print(posts)
    return posts

@app.get('/posts/{id}',response_model=schemas.PostResponse)
def get_post(id:int):
    cursor.execute("SELECT * FROM posts WHERE id=%s", (str(id),))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post('/posts',response_model=schemas.PostResponse,status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate):
    # with RETURNING clause, you can get the id of the inserted row
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ", (post.title, post.content, post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return new_post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id),))
    deleted_post=cursor.fetchone()
    
    if deleted_post==None:
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    return {"message":"Post deleted"}

@app.put('/posts/{id}',status_code=status.HTTP_200_OK)
def update_post(id:int, post: schemas.PostCreate):
    cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *", (post.title, post.content, post.published, str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    if updated_post==None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post

#*************************************************************************************************************************#
@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    try:
        # hash the password = user.password
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user=models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error while creating user {error.__cause__}")

@app.get("/users/{id}",response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    '''
    user=db.query(models.User).filter(models.User.id==id).first()
    return user
    '''
    cursor.execute("SELECT * FROM users WHERE id=%s", (str(id),))
    user=cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user 




# """
# #first part of thiss app. Without DB
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating : Optional[int] = None

#my_post = [{"title":"My first post", "content":"This is my first post", "id":1},\
           #{"title":"My second post", "content":"This is my second post", "id":2}]

# def find_post(id):
#     for p in my_post:
#         if p["id"] == id:
#             return p

# @app.get("/posts")
# def get_posts():
#     return {"data":my_post}

# @app.get("/posts/{post_id}")
# def get_post_by_id(post_id: int,response: Response):
#     target_post = find_post(post_id)
#     if not target_post:
#         raise HTTPException(status_code=404, \
#             detail="Post not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"detail":"Post not found"}
#     return {"data":target_post}

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# #we get json body as a dictionary
# def create_posts(post:Post):
#     post_dict=post.dict()
#     post_dict["id"]=len(my_post)+1
#     my_post.append(post_dict)
#     return {"data":post.dict()}
#     #return {"data":f"Succesfuly created post and your data is {new_post.content}"}

# @app.put("/posts/{post_id}")
# def update_post(post_id: int, post: Post):
#     target_post = find_post(post_id)
#     if not target_post:
#         raise HTTPException(status_code=404, \
#             detail="Post not found")
#     target_post.update(post.dict())
#     return {"data":target_post}

# @app.delete("/posts/{post_id}",status_code=204)
# def delete_post(post_id: int,):
#     target_post = find_post(post_id)
#     if not target_post: 
#         raise HTTPException(status_code=404, \
#             detail="Post not found")
#     my_post.remove(target_post)
#     #this is rule. we don't return anything
#     return Response(status_code=status.HTTP_204_NO_CONTENT,detail="Post deleted") 
   
# @app.post("/createPosts")
# #we get json body as a dictionary
# def create_posts(payload: dict =Body(...)):
#     print(payload)
#     return {"data":f"Succesfuly created post and your data is {payload['data']}"}