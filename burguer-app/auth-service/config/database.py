"""
Docstring for burguer-app.auth-service.config.database
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["burguer_app_db"]


"""
Function to get the database connection.
Args:       None
Returns:    Database connection object
db: Database connection object """


def get_db():
    return db
