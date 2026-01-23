import pytest
import os
import sys


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "auth-service"))
)

from models.user_model import serialize_user


@pytest.mark.usefixtures("mongo_db")
def test_serialize_user(mongo_db):
    user_data = {"username": "testuser", "email": "testuser@example.com"}
    result = mongo_db["users"].insert_one(user_data)
    user_from_db = mongo_db["users"].find_one({"_id": result.inserted_id})
    assert user_from_db["email"] == "testuser@example.com"
