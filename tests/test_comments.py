import pytest
from app.schemas import comments

def test_create_comment(authorized_client, test_posts, test_user):
    res = authorized_client.post(
        "/comment/", json={"post_id": test_posts[3].id, "content": "content"})

    created_comment = comments.Comment(**res.json())
    assert res.status_code == 201
    assert created_comment.content == "content"
    assert created_comment.user_id == test_user['id']
