import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    text = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    sender_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    order_id = Column(
        String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )

    sender = relationship("User", back_populates="messages")
    order = relationship("Order", back_populates="messages")
