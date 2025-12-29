import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from app.config.settings import settings

# Definir los alcances (Scopes)
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_credentials():
    """Obtiene credenciales válidas desde Variables de Entorno o Archivo Local."""
    creds = None

    # 1. Intentar cargar desde Variable de Entorno (Prioridad para Render)
    if settings.GOOGLE_TOKEN_JSON:
        try:
            token_data = json.loads(settings.GOOGLE_TOKEN_JSON)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"Error al cargar token desde variable de entorno: {e}")

    # 2. Intentar cargar desde archivo físico (Para desarrollo local)
    if not creds and os.path.exists("credentials/token.json"):
        creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)

    # 3. Refrescar el token si ha expirado
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Si estamos en local, intentamos guardar el token actualizado al disco
            if not settings.GOOGLE_TOKEN_JSON and os.path.exists("credentials"):
                with open("credentials/token.json", "w") as token:
                    token.write(creds.to_json())
        except Exception as e:
            print(f"No se pudo refrescar el token: {e}")
            creds = None

    return creds


def get_drive_service():
    """Crea y retorna el cliente de Google Drive."""
    creds = get_credentials()
    if not creds:
        raise Exception("No se pudieron obtener credenciales para Google Drive.")

    return build("drive", "v3", credentials=creds)


def upload_to_drive(file_path: str, filename: str):
    """Sube un archivo a Google Drive y devuelve el link de acceso."""
    try:
        service = get_drive_service()

        file_metadata = {"name": filename, "parents": [settings.GOOGLE_DRIVE_FOLDER_ID]}

        media = MediaFileUpload(
            file_path,
            mimetype="application/octet-stream",  # Genérico para cualquier archivo
            resumable=True,
        )

        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id, webViewLink")
            .execute()
        )

        return file.get("webViewLink")

    except Exception as e:
        print(f"Error en upload_to_drive: {str(e)}")
        raise e
