from aiogram import types
from fastapi import HTTPException, status

from app.bot.dispatcher import dp, bot
from app.api import crud, schemas, deps
from app.database.session import db


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
            await message.answer(msgs)
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
        await message.answer(text=f"Got your token, {user.username.capitalize()}!")
    except HTTPException:
        pass
