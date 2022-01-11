from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional, List
from sqlalchemy import func
from app import models,utils,schemas,oauth2
from app.database import  get_db
from sqlalchemy.orm import Session
from app.config import settings

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#@router.get('/',response_model=List[schemas.PostResponse])
@router.get('/',response_model=List[schemas.PostResponseVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit:int=10,skip:int=0,search: Optional[str] = "",):
    #cursor.execute("SELECT * FROM posts")
    #posts=cursor.fetchall()
    #print(posts)
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get('/{id}',\
    response_model=schemas.PostResponseVote)
def get_post(
    id:int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    #cursor.execute("SELECT * FROM posts WHERE id=%s", (str(id),))
    #post=cursor.fetchone()
    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post('/',response_model=schemas.PostResponse,status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, 
            db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
    # with RETURNING clause, you can get the id of the inserted row
    #cursor.execute("INSERT INTO posts (title, content, published,owner_id) VALUES (%s, %s, %s, %s) RETURNING * ", 
                    #(post.title, post.content, post.published,str(current_user.id)))                   
    #new_post=cursor.fetchone()
    #conn.commit()
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id),))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=404, detail="Post not found")
    #check user_credentials
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}',response_model=schemas.PostResponse,status_code=status.HTTP_200_OK)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *", (post.title, post.content, post.published, str(id)))
    #updated_post=cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=404, detail="Post not found")   

    if str(post.owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="You are not the owner of this post")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
  
    return post_query.first()

