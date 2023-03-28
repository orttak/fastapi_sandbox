For testing purpose, we should create testing DB for tesitng purpose.


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


