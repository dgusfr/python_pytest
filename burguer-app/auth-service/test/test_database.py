import pytest
import os


def test_get_db(mongo_db):
    """Testa se consegue obter instância do banco."""
    db = mongo_db
    assert db is not None
    assert db.name == "burguer_app_db"


def test_get_db_with_collections(mongo_db):
    """Testa se consegue criar e acessar collections."""
    db = mongo_db
    
    # Inserir um documento de teste
    result = db["test_collection"].insert_one({"test": "data"})
    assert result.inserted_id is not None
    
    # Recuperar documento
    doc = db["test_collection"].find_one({"test": "data"})
    assert doc is not None
    assert doc["test"] == "data"
