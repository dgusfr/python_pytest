import pytest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config"))
)


def test_get_db():
    with patch("database.MongoClient") as mock_mongo_client:
        mock_db = MagicMock()
        mock_mongo_client.return_value.__getitem__.return_value = mock_db

        from config.database import get_db

        with patch(
            "config.database.db", mock_mongo_client.return_value["burguer_app_db"]
        ):
            db_instance = get_db()
            assert db_instance is not None
