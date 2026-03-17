from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: str
    sender_id: str
    order_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)