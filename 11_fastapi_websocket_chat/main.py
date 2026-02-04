from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query
from auth import verify_token
from connection import connect, disconnect, broadcast
from shemas import Message

app = FastAPI()

@app.websocket("/ws/chat/")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),      # JWT token from client
    room: str = Query("general")  # room name
):
    # Authenticate user
    username = verify_token(token)
    
    # Connect to room
    await connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to all users in the room
            await broadcast(room, f"{username}: {data}")
    except WebSocketDisconnect:
        disconnect(websocket, room)
        await broadcast(room, f"{username} left the chat")

        await broadcast(room, f"{username} left the chat")
