from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL, server_api=ServerApi("1"))
db = client[DB_NAME]

companies_collection = db["companies"]


def get_db():
    """
    Get database instance.
    
    Returns:
        MongoDB database instance
    """
    return db


def get_companies_collection():
    """
    Get companies collection.
    
    Returns:
        MongoDB companies collection
    """
    return companies_collection
