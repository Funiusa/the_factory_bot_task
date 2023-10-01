from aiogram import types
from fastapi import HTTPException, status

from app.core.config import settings
from app.bot.dispatcher import dp, bot
from app.api import crud, schemas, deps
from app.database.session import db

START_MSG = f"""
Hello there! 👋

This is where you will receive messages from the API.

First you need to create your profile at the docs page, User block.
👉 http://{settings.HOST_IP}:{settings.API_PORT}/docs ⇨ /api/v1/users/open

Next you need to use the login endpoint.
Token generates on the "/api/v1/login/access_token", Login block.

Finally just copy the token and post it here.👇 
Good luck 😉
"""


@dp.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
    telegram_id = message.chat.id
    user = crud.user.get_by_telegram_id(db, telegram_id=telegram_id)
    if user:
        await message.answer(text=f"👋Hello again, {user.username}")
    else:
        await message.answer(text=START_MSG)


@dp.message_handler(commands=["messages"])
async def all_messages(message: types.Message) -> None:
    telegram_id = message.chat.id
    user = crud.user.get_by_telegram_id(db, telegram_id=telegram_id)
    if user:
        user_msgs = crud.message.get_multi_by_author(db, author_id=user.id)
        msgs = "\n\n".join([msg.body for msg in user_msgs])
        if not msgs:
            await message.answer(text="No messages yet")
        else:
            await message.answer(text=f"Messages:\n\n{msgs}")
    else:
        await message.answer("You need to send your access_token here before")


async def send_telegram_message(username: str, telegram_id: int, body: str):
    message = f"{username.capitalize()}, I got a message from you:\n\n{body}"
    await bot.send_message(chat_id=telegram_id, text=message)
    return status.HTTP_200_OK


@dp.message_handler()
async def messages_from_api(message: types.Message):
    try:
        token = message.text
        user = deps.get_current_user(db=db, token=token)
        if not user.telegram_id:
            telegram_id = message.chat.id
            user_in = schemas.UserTelegramUpdate(
                username=user.username, email=user.email, telegram_id=telegram_id
            )
            crud.user.update_with_telegram_id(db=db, db_obj=user, obj_in=user_in)

        await message.answer(text=f"Got your token, {user.username.capitalize()}! 👌")
    except HTTPException:
        pass
