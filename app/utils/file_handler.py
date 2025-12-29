import os
from app.config.settings import settings


def save_temp_file(file):
    try:
        # Crea la carpeta si no existe usando la ruta de settings
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        return file_path
    except Exception as e:
        print(f"Error guardando archivo: {e}")
        raise e


def remove_temp_file(file_path: str):
    """Elimina el archivo temporal."""
    if os.path.exists(file_path):
        os.remove(file_path)
