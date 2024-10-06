from fastapi import Depends, FastAPI, WebSocket, UploadFile, File
from app.db.postgres import get_db, metadata, Base, engine
from celery_worker import process_file
import shutil
from app.services.file_upload import router as upload_router
app = FastAPI()

# Initialize the database
Base.metadata.create_all(bind=engine)

app.include_router(upload_router)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")
