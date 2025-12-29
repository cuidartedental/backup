import os.path
from google.auth.transport.requests import Request
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from app.config.settings import settings
import os

# Solo necesitamos permiso para archivos creados por la app
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_drive_service():
    creds = None

    # RUTA SENIOR: Intentar cargar token desde variable de entorno primero
    token_data = os.getenv("GOOGLE_TOKEN_JSON")

    if token_data:
        # Cargamos las credenciales directamente desde el string JSON
        creds_info = json.loads(token_data)
        creds = Credentials.from_authorized_user_info(creds_info, SCOPES)

    # Si no hay variable (desarrollo local), buscar archivo físico
    elif os.path.exists("credentials/token.json"):
        creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)

    # Si el token expiró y tenemos client_secrets, refrescamos
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request

            creds.refresh(Request())
        else:
            # En producción (Render), esto fallaría porque no hay interfaz gráfica
            # Por eso es vital subir el GOOGLE_TOKEN_JSON inicial
            raise Exception(
                "No hay token válido. Genera el token.json localmente primero."
            )

    return build("drive", "v3", credentials=creds)


def upload_to_drive(file_path: str, filename: str) -> str:
    try:
        service = get_drive_service()
        file_metadata = {"name": filename, "parents": [settings.GOOGLE_DRIVE_FOLDER_ID]}
        media = MediaFileUpload(file_path, resumable=True)

        # Ya no necesitamos supportsAllDrives porque ahora eres TÚ quien sube
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id, webViewLink")
            .execute()
        )

        return file.get("webViewLink")
    except Exception as e:
        print(f"Error subiendo a Drive: {e}")
        return None


def list_drive_files():
    try:
        service = get_drive_service()
        query = f"'{settings.GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed = false"
        results = (
            service.files()
            .list(q=query, pageSize=20, fields="files(id, name, webViewLink)")
            .execute()
        )
        return results.get("files", [])
    except Exception as e:
        print(f"Error listando: {e}")
        return []
