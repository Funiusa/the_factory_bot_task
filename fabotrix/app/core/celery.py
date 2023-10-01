from celery import Celery
from app.core.config import settings
from app.bot.handlers.message_handler import send_telegram_message
import asyncio

celery_app = Celery(__name__)

celery_app.conf.broker_url = settings.BROKER
celery_app.conf.result_backend = settings.CELERY_RESULT_BACKEND


@celery_app.task(serializer="json")
def send_message_to_telegram(username: str, telegram_id: int, body: str):
    loop = asyncio.get_event_loop()
    coro = send_telegram_message(username, telegram_id, body)
    message = loop.run_until_complete(coro)
    return {"status": message}
