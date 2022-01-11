from fastapi import FastAPI, Response,status, HTTPException,Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor

from app import models,utils,schemas
from app.database import  engine ,get_db
from sqlalchemy.orm import Session
from app.config import settings

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
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

@router.get("/{id}",response_model=schemas.UserOut)
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