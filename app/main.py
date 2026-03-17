from typing import List

from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.core.security import verify_password, create_access_token
from app.core.ws_manager import manager
from app.crud.message import create_message, get_messages_by_order
from app.crud.order import create_order, get_user_orders
from app.crud.user import get_user_by_email, create_user
from app.models.user import User
from app.schemas.message import MessageCreate, MessageResponse
from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse

app = FastAPI(
    title="B2B Order Messaging Service",
    description="Core API for B2B orders and real-time communication",
    version="0.1.0"
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for container orchestration and monitoring."""
    return {"status": "ok", "message": "B2B Service is up and running!"}


# --- Users ---

@app.post("/users/register", response_model=UserResponse, tags=["Users"])
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db=db, user=user)


@app.post("/users/login", response_model=Token, tags=["Users"])
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserResponse, tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# --- Orders ---

@app.post("/orders", response_model=OrderResponse, tags=["Orders"])
async def create_new_order(
        order: OrderCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await create_order(db=db, order=order, current_user=current_user)


@app.get("/orders", response_model=List[OrderResponse], tags=["Orders"])
async def read_user_orders(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await get_user_orders(db=db, current_user=current_user)


# --- Messages ---

@app.post("/orders/{order_id}/messages", response_model=MessageResponse, tags=["Messages"])
async def send_message(
        order_id: str,
        message: MessageCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Save a new message to the database and broadcast it to all active WebSocket clients in the order room."""
    db_message = await create_message(db=db, message=message, order_id=order_id, current_user=current_user)

    message_data = {
        "id": str(db_message.id),
        "text": db_message.text,
        "sender_id": str(db_message.sender_id),
        "order_id": str(db_message.order_id),
        "created_at": db_message.created_at.isoformat()
    }

    await manager.broadcast_to_order(message_data=message_data, order_id=order_id)

    return db_message


@app.get("/orders/{order_id}/messages", response_model=List[MessageResponse], tags=["Messages"])
async def read_messages(
        order_id: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await get_messages_by_order(db=db, order_id=order_id)


# --- WebSockets ---

@app.websocket("/ws/orders/{order_id}")
async def websocket_endpoint(websocket: WebSocket, order_id: str):
    """Establish a persistent WebSocket connection for real-time order communication."""
    await manager.connect(websocket, order_id)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, order_id)