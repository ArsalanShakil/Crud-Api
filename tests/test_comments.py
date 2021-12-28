import pytest
from app.schemas import comments

def test_create_comment(authorized_client, test_posts, test_user):
    res = authorized_client.post(
        "/comment/", json={"post_id": test_posts[3].id, "content": "content"})

    created_comment = comments.Comment(**res.json())
    assert res.status_code == 201
    assert created_comment.content == "content"
    assert created_comment.user_id == test_user['id']

def test_unauthorized_user_create_comment(client, test_user, test_posts):
    res = client.post(
        "/comment/", json={"post_id": test_posts[3].id, "content": "content"})
    assert res.status_code == 401
    

def test_delete_comment_non_exist(authorized_client, test_user, test_posts):

    res = authorized_client.delete(
        f"/comment/8000000")

    assert res.status_code == 404
    
# def test_update_comment(authorized_client, test_posts, test_user):
#     res = authorized_client.put(
#         "/comment/", json={"content": "content update"})

#     update_comment = comments.CommentUpdate(**res.json())
#     assert res.status_code == 200
#     assert update_comment.content == "content update"
