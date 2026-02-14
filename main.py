from fastapi import FastAPI
from config import MONGO_URL, DB_NAME

app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Server is running",
        "mongo_url_loaded": bool(MONGO_URL),
        "db_name": DB_NAME
    }
