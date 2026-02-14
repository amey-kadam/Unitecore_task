from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL, server_api=ServerApi("1"))
db = client[DB_NAME]

def get_db():
    return db
