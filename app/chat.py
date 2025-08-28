from fastapi import APIRouter, WebSocket
from typing import List

router = APIRouter(prefix="/chat", tags=["Chat"])
active_connections: List[WebSocket] = []

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for connection in active_connections:
                if connection != websocket:
                    await connection.send_text(f"{username}: {data}")
    except:
        active_connections.remove(websocket)
