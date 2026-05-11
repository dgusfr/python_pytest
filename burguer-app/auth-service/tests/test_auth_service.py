import pytest
from werkzeug.security import generate_password_hash

from services.auth_service import login_user, users_col


def test_login_user_success(mongo_db):
    users_col.delete_many({})
    users_col.insert_one(
        {
            "email": "user@example.com",
            "password": generate_password_hash("secret"),
            "name": "Test User",
            "role": "cliente",
        }
    )

    res = login_user("user@example.com", "secret")
    assert isinstance(res, dict)
    assert res["email"] == "user@example.com"
    assert "token" in res


def test_login_user_failure_wrong_password(mongo_db):
    users_col.delete_many({})
    users_col.insert_one(
        {
            "email": "user@example.com",
            "password": generate_password_hash("secret"),
        }
    )

    assert login_user("user@example.com", "bad") is None


def test_login_user_failure_no_user(mongo_db):
    users_col.delete_many({})
    assert login_user("missing@example.com", "any") is None
