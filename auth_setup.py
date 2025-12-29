from app.services.google_drive import get_drive_service

print("Iniciando autenticación manual...")
get_drive_service()
print("✅ Token generado con éxito.")
