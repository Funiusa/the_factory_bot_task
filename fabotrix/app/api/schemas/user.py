from pydantic import BaseModel, Field
from .message import Message


class UserBase(BaseModel):
    username: str = Field(default="example")
    email: str = Field(default="example@mail.com")
    is_active: bool | None = True
    is_superuser: bool = False


class UserCreate(UserBase):
    username: str
    email: str
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserTelegramUpdate(UserBase):
    telegram_id: int | None = None


class UserInDBBase(UserBase):
    id: int | None = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    telegram_id: int | None = None
    messages: list[Message] = None


class UserInDB(UserInDBBase):
    hashed_password: str
