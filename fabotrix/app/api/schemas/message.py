from datetime import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    body: str | None = None


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class MessageInDBBase(MessageBase):
    id: int
    body: str
    author_id: int
    creation_date: datetime

    class Config:
        orm_mode = True


class Message(MessageInDBBase):
    pass


class MessageInDB(MessageInDBBase):
    pass
