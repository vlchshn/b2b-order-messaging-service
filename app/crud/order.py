from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate


async def create_order(
    db: AsyncSession, order: OrderCreate, current_user: User
) -> Order:
    """Create a new order and associate it with the current user."""
    db_order = Order(
        title=order.title, description=order.description, owner_id=current_user.id
    )

    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    return db_order


async def get_user_orders(db: AsyncSession, current_user: User) -> list[Order]:
    """Retrieve all orders owned by the current user."""
    result = await db.execute(select(Order).where(Order.owner_id == current_user.id))
    return list(result.scalars().all())
