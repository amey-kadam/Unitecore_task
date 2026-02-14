from fastapi import FastAPI

app = FastAPI(title="Company CRUD API")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running"}
