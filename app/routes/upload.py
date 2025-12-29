import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks

# Importamos los servicios
from app.services.google_drive import upload_to_drive
from app.services.telegram_bot import send_to_telegram
from app.services.notifications import notify_success
from app.utils.file_handler import save_temp_file, remove_temp_file

router = APIRouter()

# Creamos un ejecutor para hilos (Senior Practice)
executor = ThreadPoolExecutor(max_workers=3)


@router.post("/upload/drive")
async def upload_file_to_drive(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    temp_path = save_temp_file(file)
    loop = asyncio.get_event_loop()

    try:
        # Ejecutamos la subida síncrona en un hilo separado para no congelar FastAPI
        drive_link = await loop.run_in_executor(
            executor, upload_to_drive, temp_path, file.filename
        )

        if not drive_link:
            raise HTTPException(status_code=502, detail="Error en Drive")

        background_tasks.add_task(
            notify_success, file.filename, "Google Drive", f"Link: {drive_link}"
        )
        return {"status": "Success", "link": drive_link}
    finally:
        background_tasks.add_task(remove_temp_file, temp_path)


@router.post("/upload/telegram")
async def upload_file_to_telegram(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    """
    Recibe un archivo y lo envía exclusivamente al Bot de Telegram.
    """
    # 1. Guardar archivo temporalmente
    try:
        temp_path = save_temp_file(file)
    except Exception:
        raise HTTPException(status_code=500, detail="Error al guardar archivo temporal")

    try:
        # 2. Subir a Telegram (Async)
        telegram_success = await send_to_telegram(
            temp_path, caption=f"📂 Archivo recibido: {file.filename}"
        )

        if not telegram_success:
            raise HTTPException(status_code=502, detail="Fallo el envío a Telegram")

        return {"filename": file.filename, "service": "Telegram", "status": "Success"}

    finally:
        # 3. Limpieza (Background Task)
        background_tasks.add_task(remove_temp_file, temp_path)
