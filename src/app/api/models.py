from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

#from app.db import Base

class NoteSchema(BaseModel):
    title: str
    description: str

class NoteDB(NoteSchema):
    id: int
    class Config:
        orm_mode = True