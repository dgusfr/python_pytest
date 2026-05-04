"""
Database connection factory with test-friendly behavior.

In tests, when the environment variable USE_MOCK_DB=1 is set (default via
conftest), an in-memory mongomock client is used to avoid external
connections. In all other cases, a real MongoDB client is created using
MONGO_URI (or localhost by default).
"""

import os
from dotenv import load_dotenv

load_dotenv()

_USE_MOCK = os.getenv("USE_MOCK_DB") == "1" or bool(os.getenv("PYTEST_CURRENT_TEST"))
_MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "burguer_app_db")

_db = None

if _USE_MOCK:
    try:
        import mongomock  # type: ignore

        _client = mongomock.MongoClient()
        _db = _client[_MONGO_DB_NAME]
    except Exception:
        _USE_MOCK = False

if not _USE_MOCK:
    from pymongo import MongoClient  # type: ignore

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    _db = _client[_MONGO_DB_NAME]


def get_db():
    """Return the database handle for the application."""
    return _db
