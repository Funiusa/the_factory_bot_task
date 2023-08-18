from typing import List
from sqlalchemy.orm import Session
from fastapi import status, Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from app.api import deps, schemas, crud, models
from app.bot.handlers.message_handler import send_message_to_telegram

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Message])
def get_messages(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(deps.get_session),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> List[schemas.Message]:
    if crud.user.is_superuser(current_user):
        messages = crud.message.get_multi(db=session, skip=skip, limit=limit)
    else:
        messages = crud.message.get_multi_by_author(
            db=session, author_id=current_user.id, skip=skip, limit=limit
        )
    return messages


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Message)
async def create_message(
        *,
        message: str,
        session: Session = Depends(deps.get_session),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.Message:
    telegram_id = current_user.telegram_id
    if not telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need to add your access_token in telegram chat before"
        )
    message_in = schemas.MessageCreate(body=message)
    message = crud.message.create_with_author(
        db=session, obj_in=message_in, author_id=current_user.id
    )
    await send_message_to_telegram(
        username=current_user.username,
        telegram_id=current_user.telegram_id,
        body=message.body,
    )
    return message


@router.put(
    "/{message_id}", status_code=status.HTTP_200_OK, response_model=schemas.Message
)
def update_message(
        *,
        message_id: int,
        message_in: schemas.MessageUpdate,
        session: Session = Depends(deps.get_session),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.Message:
    message = crud.message.get(db=session, id=message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    if (
            not crud.user.is_superuser(current_user)
            and message.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission"
        )
    updated_message = crud.message.update(session, db_obj=message, obj_in=message_in)
    return updated_message


@router.get(
    "/{message_id}", status_code=status.HTTP_200_OK, response_model=schemas.Message
)
def retrieve_message(
        *,
        message_id: int,
        session: Session = Depends(deps.get_session),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.Message:
    message = crud.message.get(session, id=message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    if (
            not crud.user.is_superuser(current_user)
            and message.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission"
        )
    return message


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_message(
        *,
        message_id: int,
        session: Session = Depends(deps.get_session),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> None:
    post = crud.message.get(session, id=message_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    if not crud.user.is_superuser(current_user) and post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission"
        )
    crud.message.remove(db=session, id=message_id)
