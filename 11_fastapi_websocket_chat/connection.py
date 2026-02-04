from fastapi import WebSocket
from collections import defaultdict

active_connections: dict[str, list[WebSocket]] = defaultdict(list)

async def connect(websocket: WebSocket, room: str):
    await websocket.accept()
    active_connections[room].append(websocket)

def disconnect(websocket: WebSocket, room: str):
    active_connections[room].remove(websocket)

async def broadcast(room: str, message: str):
    for connection in active_connections[room]:
        await connection.send_text(message)
