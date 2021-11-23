from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    #use inheritance to add the id field
    id:int
    created_at: datetime
    # convert sqlchemy object to pydantic object
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True