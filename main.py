from fastapi import FastAPI
from app.database import get_db, get_companies_collection
from app.routes.company import router as company_router
from config import MONGO_URL, DB_NAME

app = FastAPI(
    title="Company Management API",
    description="CRUD API for managing company registrations with MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(company_router)

@app.on_event("startup")
async def startup_event():
    try:
        companies_collection = get_companies_collection()
        companies_collection.create_index("email", unique=True)
        companies_collection.create_index("mobile", unique=True)
        print("MongoDB indexes created successfully")
    except Exception as e:
        print(f"Warning: Could not create MongoDB indexes: {e}")



@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "message": "Server is running",
        "mongo_url_loaded": bool(MONGO_URL),
        "db_name": DB_NAME
    }

