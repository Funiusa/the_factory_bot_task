from sqlalchemy.orm import Session
from app.api import crud, schemas
from app.core.config import settings
from .base_class import Base
from .session import engine, SessionLocal


def init(db: Session) -> None:
    Base.metadata.create_all(engine)
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email=settings.FIRST_SUPERUSER_EMAIL,
            is_superuser=True,
            is_active=True,
        )
        user = crud.user.create(db, obj_in=user_in)


def init_db() -> None:
    db = SessionLocal()
    init(db)
