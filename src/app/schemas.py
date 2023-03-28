from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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
    
    owner_id: int
    owner: UserOut
    # convert sqlchemy object to pydantic object
    class Config:
        orm_mode = True
#basemodel degil de PostBase alirsak calismadi
class PostResponseVote(BaseModel):
    Post:PostResponse
    votes:int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)