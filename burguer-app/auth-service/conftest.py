import pytest
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def mongo_client():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    yield client
    client.close()
