# app/main.py
from fastapi import FastAPI
from app.routes import upload
from app.config.settings import settings

from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="Dental Backup API")
app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Configuración de CORS
origins = [
    "https://cuidarte-backup.netlify.app",
    "https://cuidarte-backup.netlify.app/",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Incluir rutas
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])


@app.get("/")
def read_root():
    return {"message": "API Backend is running"}
