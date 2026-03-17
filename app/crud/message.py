from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate


async def create_message(
    db: AsyncSession, message: MessageCreate, order_id: str, current_user: User
) -> Message:
    """Create a new message linked to an order and the current user."""
    db_message = Message(
        text=message.text, sender_id=current_user.id, order_id=order_id
    )

    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)

    return db_message


async def get_messages_by_order(db: AsyncSession, order_id: str) -> list[Message]:
    """Retrieve all messages for a specific order, sorted chronologically."""
    result = await db.execute(
        select(Message)
        .where(Message.order_id == order_id)
        .order_by(Message.created_at.asc())
    )
    return list(result.scalars().all())
