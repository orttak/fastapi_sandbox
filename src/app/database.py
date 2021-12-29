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
from app.config import settings
#DATABASE_URL = os.getenv("DATABASE_URL")

#SQL_DATABASE_URL ='postgresql://username:paswword@ipAdress/hostname/databasename'
#SQL_DATABASE_URL='postgresql://hello_fastapi:hello_fastapi@db/hello_fastapi_dev'
#SQL_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:/{settings.database_name}'
SQL_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#SQL_DATABASE_URL=settings.database_full_name
print(SQL_DATABASE_URL)
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
#for postgres connection
# try:
#     #if you work with docker compose, host name should be db from docker-compose.yml
#     conn = psycopg2.connect(
#         dbname="hello_fastapi_dev",
#         user="hello_fastapi",
#         password="hello_fastapi",
#         host="db",
#         port="5432",
#         cursor_factory=RealDictCursor)
#     cursor=conn.cursor()
# except Exception as error:
#     print("Error while connecting to the database")
#     print(f"Error is {error}")

