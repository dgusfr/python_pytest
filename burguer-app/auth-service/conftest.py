import os
import pytest
from dotenv import load_dotenv

# Prefer an in-memory MongoDB for tests to avoid network calls
mongomock = None  # type: ignore
try:
    import mongomock as _mongomock  # type: ignore

    mongomock = _mongomock
    _HAS_MONGOMOCK = True
except Exception:  # pragma: no cover - fallback when package missing
    _HAS_MONGOMOCK = False
    from pymongo import MongoClient  # type: ignore

load_dotenv()


@pytest.fixture(scope="session")
def mongo_client():
    """Provide a Mongo client for tests.

    Defaults to an in-memory mongomock client when available, unless
    USE_REAL_MONGO=1 is set in the environment.
    """
    use_real = os.getenv("USE_REAL_MONGO") == "1"

    if _HAS_MONGOMOCK and not use_real:
        client = mongomock.MongoClient()  # type: ignore[attr-defined]
    else:
        # Fall back to a real client (requires local MongoDB)
        # Intentionally ignore MONGO_URI to avoid remote connections in tests.
        from pymongo import MongoClient  # local import to avoid import at module load

        mongo_uri = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017")
        client = MongoClient(mongo_uri)

    try:
        yield client
    finally:
        # mongomock has no close side effects, but this is safe for both
        client.close()


@pytest.fixture(scope="function")
def mongo_db(mongo_client):
    db = mongo_client["test_db"]
    db["users"].delete_many({})
    db["pedidos"].delete_many({})
    yield db
    mongo_client.drop_database("test_db")
