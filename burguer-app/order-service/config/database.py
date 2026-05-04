from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura conexão com fallback para ambiente local via Docker
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongo_db_name = os.getenv("MONGO_DB_NAME", "burguer_app_db")

# Cria a conexão com o banco de dados MongoDB
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

# Seleciona o banco de dados
db = client[mongo_db_name]

# função para retornar a instância do banco de dados
def get_db():
    return db
