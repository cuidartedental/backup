# app/main.py
from fastapi import FastAPI
from app.routes import upload
from app.config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Incluir rutas
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])


@app.get("/")
def read_root():
    return {"message": "API Backend is running"}
