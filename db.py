from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL, server_api=ServerApi("1"))
db = client[DB_NAME]

companies_collection = db["companies"]

companies_collection.create_index("email", unique=True)
companies_collection.create_index("mobile", unique=True)

def get_db():
    return db

def get_companies_collection():
    return companies_collection
