from typing import List
import pytest
from app import schemas

def test_get_all_posts(authorized_client,test_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200

def test_user_get_one_post(authorized_client,test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0]['owner_id']}")
    post=schemas.PostResponseVote(**response.json())
    assert post.Post.id == test_posts[0]['owner_id']
    assert response.status_code == 200

def test_get_one_post_not_exist(authorized_client):
    response = authorized_client.get(f"/posts/0")
    assert response.status_code == 404

def test_unautharize_post(client,test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorize_user_get_one_post(client,test_posts):
    response = client.get(f"/posts/{test_posts[0]['owner_id']}")
    assert response.status_code == 401


@pytest.mark.parametrize(
    #define variables for pytest 
    "title,content,published", [
    ("test_post v1", "test_content v1", True),
    ("test_post v2 ", "test_content v2", False),
    ("test_post v3", "test_content v3", True)])
def test_create_post(authorized_client,test_user,title,content, published):

    response= authorized_client.post("/posts/", json={"title":title, "content":content, "published":published})
    created_post=schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]

def test_unauthorize_post(client):
    response= client.post("/posts/", json={"title":'title', "content":'content', "published":True})
    assert response.status_code == 401

def test_authorize_delete_post(authorized_client,test_posts):
    response= authorized_client.delete(f"/posts/{test_posts[0]['owner_id']}")
    assert response.status_code == 204

def test_unauthorize_delete_post(client,test_posts):
    response= client.delete(f"/posts/{test_posts[0]['owner_id']}")
    assert response.status_code == 401

def test_authorize_delete_non_exist_post(authorized_client):
    response=authorized_client.delete(f"/posts/{0}")
    assert response.status_code == 404

def test_authorize_delete_other_user_post(authorized_client,test_user,test_posts):
    response=authorized_client.delete(
        f"/posts/4")
    assert response.status_code == 403

def test_update_post(authorized_client,test_user,test_posts):
    data={"title":'updated_title', "content":'updated_content', 'id':test_posts[0]['owner_id']}
    response=authorized_client.put(f"/posts/{test_posts[0]['owner_id']}",json=data)
    updated_post=schemas.PostResponse(**response.json())  
    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_client_post(authorized_client,test_user,test_posts):
    data={"title":'updated_title', "content":'updated_content', 'id':test_posts[0]['owner_id']}
    response=authorized_client.put(f"/posts/4",json=data)
    assert response.status_code == 403

def test_update_non_exist_post(authorized_client,test_user,test_posts):
    data={"title":'updated_title', "content":'updated_content', 'id':test_posts[0]['owner_id']}
    response=authorized_client.put(f"/posts/0",json=data)
    assert response.status_code == 404