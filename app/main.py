from fastapi import Depends, FastAPI, WebSocket, UploadFile, File
from app.db.postgres import get_db, metadata, Base, engine
from app.tasks import process_file
from sqlalchemy.orm import Session
import shutil

app = FastAPI()

# Initialize the database
Base.metadata.create_all(bind=engine)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    # Enqueue file processing task with Celery
    task = process_file.delay(file_location)
    
    return {"filename": file.filename, "task_id": task.id}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")
