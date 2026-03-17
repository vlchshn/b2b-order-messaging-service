import time

from celery import Celery

from app.core.config import settings

celery_app = Celery("b2b_tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
)


@celery_app.task(name="process_order")
def process_order_background(order_id: str, user_email: str) -> str:
    """
    Simulate heavy background processing such as PDF invoice generation
    and sending confirmation emails to the client without blocking the main event loop.
    """
    # Simulated I/O-bound operations
    time.sleep(3)

    return (
        f"Order {order_id} successfully processed. Confirmation sent to {user_email}."
    )
