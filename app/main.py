from fastapi import FastAPI, WebSocket
from app.db.postgres import Base, engine
from app.services.file_upload import router as upload_router
from app.services.anamoly_list import router as anamoly_router
app = FastAPI()

# Initialize the database
Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(upload_router)
app.include_router(anamoly_router)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")
