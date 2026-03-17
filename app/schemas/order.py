from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    title: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: str
    status: str
    owner_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
