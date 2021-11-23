import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from databases import Database

#DATABASE_URL = os.getenv("DATABASE_URL")

#SQL_DATABASE_URL ='postgresql://username:paswword@ipAdress/hostname/databasename'
SQL_DATABASE_URL='postgresql://hello_fastapi:hello_fastapi@db/hello_fastapi_dev'
engine = create_engine(SQL_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()
'''
Create a Base class¶
Now we will use the function declarative_base() that returns a class.
Later we will inherit from this class to create each of the database models or classes (the ORM models):
'''

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

