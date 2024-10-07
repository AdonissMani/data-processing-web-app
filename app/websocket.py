from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import FastAPI
from celery.result import AsyncResult

app = FastAPI()

# WebSocket manager to manage multiple clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await manager.connect(websocket)
    
    try:
        while True:
            # Periodically check Celery task status
            task_result = AsyncResult(task_id)
            if task_result.state == "SUCCESS":
                await manager.send_message(f"Anomalies detected: {task_result.result}")
                break
            await websocket.send_text(f"Task status: {task_result.state}")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
