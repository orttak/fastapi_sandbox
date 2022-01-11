from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from typing import Optional, List

from app import models,utils,schemas,oauth2,database
from app.database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED, )
def vote(vote: schemas.Vote,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    vote_query=db.query(models.Vote).filter(
        models.Vote.post_id==vote.post_id).filter(models.Vote.user_id==current_user.id)
    
    found_vote=vote_query.first()
    print(found_vote)
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f" User {current_user.id} already voted for post {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Vote created successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Vote deleted successfully"}