# app/config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # --- METADATOS DEL PROYECTO ---
    PROJECT_NAME: str = "Sistema de Respaldo Dental"

    # --- CARPETAS ---
    # Definimos la carpeta temporal para archivos
    UPLOAD_DIR: str = "uploads"

    # --- CONFIGURACIÓN DE GOOGLE DRIVE ---
    # ID de la carpeta destino en Drive
    GOOGLE_DRIVE_FOLDER_ID: str

    # En Render, pegaremos el contenido de los JSON aquí (como texto)
    GOOGLE_TOKEN_JSON: Optional[str] = None
    GOOGLE_CLIENT_SECRETS_JSON: Optional[str] = None

    # En local, usaremos esta ruta de archivo
    GOOGLE_CREDENTIALS_FILE: str = "credentials/client_secrets.json"

    # --- CONFIGURACIÓN DE TELEGRAM ---
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str

    # --- CONFIGURACIÓN DE EMAIL (SMTP) ---
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str  # Tu correo emisor
    SMTP_PASS: str  # Tu contraseña de aplicación de 16 caracteres
    EMAIL_RECEIVER: str  # Correo que recibirá la notificación

    class Config:
        # Pydantic buscará estas variables en un archivo .env si existe
        env_file = ".env"
        # Permite que haya más variables en el .env de las que definimos aquí
        extra = "ignore"


# Instancia única para ser importada en todo el proyecto
settings = Settings()
