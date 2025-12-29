# app/services/telegram_bot.py
import httpx
from app.config.settings import settings


async def send_to_telegram(file_path: str, caption: str = "") -> bool:
    """Envía un documento a un chat de Telegram."""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendDocument"

    try:
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as f:
                files = {"document": (os.path.basename(file_path), f)}
                data = {"chat_id": settings.TELEGRAM_CHAT_ID, "caption": caption}

                response = await client.post(url, data=data, files=files)

                if response.status_code == 200:
                    return True
                else:
                    print(f"Error Telegram: {response.text}")
                    return False
    except Exception as e:
        print(f"Excepción Telegram: {e}")
        return False


import os  # Necesario para os.path.basename
