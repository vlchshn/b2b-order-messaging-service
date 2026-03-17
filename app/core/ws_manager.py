from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, order_id: str):
        """Accept a new WebSocket connection and assign it to an order room."""
        await websocket.accept()
        if order_id not in self.active_connections:
            self.active_connections[order_id] = []
        self.active_connections[order_id].append(websocket)

    def disconnect(self, websocket: WebSocket, order_id: str):
        """Remove a WebSocket connection and clean up empty rooms."""
        if order_id in self.active_connections:
            self.active_connections[order_id].remove(websocket)
            if not self.active_connections[order_id]:
                del self.active_connections[order_id]

    async def broadcast_to_order(self, message_data: dict, order_id: str):
        """Broadcast a JSON payload to all active clients in a specific order room."""
        if order_id in self.active_connections:
            for connection in self.active_connections[order_id]:
                await connection.send_json(message_data)


manager = ConnectionManager()
