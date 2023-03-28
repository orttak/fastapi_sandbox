from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base
from app import models
from app.oauth2 import create_access_token
'''
Define pytest fixture in this file.
All pytest modules can reach below functions without having to import them.

You can create different confest.py files in different places in your project.
like:
src/tests/blog/conftest.py
src/tests/api/conftest.py
'''
# at the end of the URL we define our test database
SQL_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
print(SQL_DATABASE_URL) # postgresql://hello_fastapi:hello_fastapi@db:5432/hello_fastapi_dev_test
engine = create_engine(SQL_DATABASE_URL)
TestingSessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    #before running test session, we drop all  tables and create new tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db    
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    #define client for testing. we return client with yield because before testing we prepare new env for testing
    #and after testing we clean env
    def overrite_get_db():
        db=TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrite_get_db
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data={"email":"user1@user.com", "password": "user1"}
    response = client.post(
        "/users/", json=user_data)
    assert response.status_code ==201
    new_data=response.json()
    new_data["password"]=user_data["password"]
    return new_data

@pytest.fixture()
def test_user2(client):
    user_data={"email":"user2@user.com", "password": "user2"}
    response = client.post(
        "/users/", json=user_data)
    assert response.status_code ==201
    new_data=response.json()
    new_data["password"]=user_data["password"]
    return new_data
#we create this token for testing purposes
@pytest.fixture()
def token(test_user):
    return create_access_token({'user_id':test_user["id"]})
#using this token we update our headers and test our api
# Shoud we change the scope of this fixture because we have many app which are use authorized client
# so I think we need to change scope to module. Ask to Zafer
@pytest.fixture()
def authorized_client(client,token):
    client.headers["Authorization"]=f"Bearer {token}"
    return client

@pytest.fixture()
def test_posts(test_user,test_user2,session):
    post_data=[{"title":"test_post", "content":"test_content", "owner_id":test_user["id"]},
               {"title":"test_post2", "content":"test_content2", "owner_id":test_user["id"]},
               {"title":"test_post3", "content":"test_content3", "owner_id":test_user["id"]},
               {"title":"test_post4", "content":"test_content4", "owner_id":test_user2["id"]}]
    def create_post_model(data):
        post=models.Post(**data)    
        return post
    post_map=map(create_post_model,post_data)
    posts=list(post_map)
    session.add_all(posts)
    session.commit()
    return post_data