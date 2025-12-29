# diag_drive.py
from app.services.google_drive import get_drive_service
from app.config.settings import settings


def check_access():
    service = get_drive_service()
    folder_id = settings.GOOGLE_DRIVE_FOLDER_ID
    try:
        folder = (
            service.files()
            .get(
                fileId=folder_id, fields="capabilities, owners", supportsAllDrives=True
            )
            .execute()
        )
        print(f"✅ Conexión exitosa.")
        print(f"📁 Dueño de la carpeta: {folder['owners'][0]['displayName']}")
        print(
            f"🔑 ¿Puede el robot escribir?: {folder['capabilities']['canAddChildren']}"
        )
    except Exception as e:
        print(f"❌ Error de acceso: {e}")


if __name__ == "__main__":
    check_access()
