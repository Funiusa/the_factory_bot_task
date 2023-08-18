import logging

from aiogram import executor
from aiogram.dispatcher import Dispatcher

from app.bot.utils.set_default_commands import set_default_commands
from app.bot.handlers import dp


async def on_startup(dispatcher: Dispatcher):
    await set_default_commands(dispatcher)


def start_bot():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        reset_webhook=True,
    )


if __name__ == "__main__":
    start_bot()
