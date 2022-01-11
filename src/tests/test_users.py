from fastapi.testclient import TestClient
import pytest
from jose import JWTError, jwt
from app import schemas
from app.main import app
from app.config import settings

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}

def test_create_user(client):
    response = client.post(
        "/users/", json={"email":"user1@user.com", "password": "user1"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "user1@user.com"
    assert response.status_code == 201
# if you run upper test, first you can get an error after firts calling because we save the test user in the database
# and after second call we get an error because the user is already in the database so 
# we need to delete the user before we can create a new one. we'll do it with pytest.fixture

def test_login(client,test_user):
    #we should call create test user function again because pytest.fixture scope. if we don't define scope we'll get an error
    # because user'll delete it before we start this test
    # For general purpose, we add scope definition into decarator> @pytest.fixture(scope="module") it means, each test.py call it once
    # or decorator> @pytest.fixture(scope="session") it means each test session this fixture calling it once
    # our solution is to call create test user function again
    response = client.post(
        "/login", data={"username":test_user["email"], "password":test_user["password"]})
    
    login_res=schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@user.com", "user1", 403),
    ("user1@user.com", "user2", 403),
    ("wrongemail@user.com", "user2", 403),
    (None, "user1", 422),
    ("user1@user.com",None,422)
])
def test_login_fail(test_user,client,email, password, status_code):
    response = client.post(
        "/login", data={"username":email, "password":password})
    
    assert response.status_code == status_code