# app/services/notifications.py
import httpx
import aiosmtplib
from email.message import EmailMessage
from app.config.settings import settings


async def notify_success(filename: str, service_name: str, extra_info: str = ""):
    """
    Función orquestadora que envía notificaciones a múltiples canales.
    """
    message = f"✅ Subida Exitosa\n\nArchivo: {filename}\nServicio: {service_name}\nInfo: {extra_info}"

    # 1. Notificar a Telegram (Solo texto)
    await send_telegram_text(message)

    # 2. Notificar por Correo Electrónico
    await send_email_notification(f"Éxito: {filename}", message)


async def send_telegram_text(text: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                url, json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": text}
            )
        except Exception as e:
            print(f"Error enviando texto a Telegram: {e}")


async def send_email_notification(subject: str, content: str):
    msg = EmailMessage()
    msg["From"] = settings.SMTP_USER
    msg["To"] = settings.EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.set_content(content)

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASS,
            start_tls=True,
        )
    except Exception as e:
        print(f"Error enviando email: {e}")
