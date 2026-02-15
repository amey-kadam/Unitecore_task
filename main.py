from fastapi import FastAPI
from app.database import get_db, get_companies_collection
from config import MONGO_URL, DB_NAME

app = FastAPI(
    title="Company Management API",
    description="CRUD API for managing company registrations with MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/health")
def health_check():
    """Health check endpoint to verify server and database connection"""
    return {
        "status": "ok",
        "message": "Server is running",
        "mongo_url_loaded": bool(MONGO_URL),
        "db_name": DB_NAME
    }
