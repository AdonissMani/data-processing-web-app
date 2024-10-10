from datetime import datetime
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import FileUpload, SensorData
from app.db.postgres import get_db
from pydantic import BaseModel, ValidationError
import json

from celery_worker import process_sensor_data

# Create a router instance
router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Example schema definition for the uploaded JSON
class SensorDataSchema(BaseModel):
    sensor_id: str
    value: float
    timestamp: str

# Dependency function to check the file size
def validate_file_size(file: UploadFile) -> UploadFile:
    """
    Validate the size of an uploaded file.

    Args:
    file (UploadFile): The uploaded file to validate.

    Returns:
    UploadFile: The validated file.

    Raises:
    HTTPException: If the file size exceeds the 10MB limit.
    """
    # Check the file size against the maximum allowed (10MB)
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 10MB limit.")
    # Return the validated file
    return file

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads a JSON file containing sensor data and stores it in the database.
    The file is validated against a Pydantic schema and the contents are
    stored in the SensorData table.

    Args:
    file (UploadFile): The uploaded file.
    db (Session): The database session.

    Returns:
    dict: A dictionary containing the status of the upload and the task ID
          of the Celery task for anomaly detection.
    """
    # Ensure the file is a JSON file
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid file format. Only JSON files are allowed.")
    
    try:
        # Validate the file size
        file = validate_file_size(file)

        # Upload the file to db
        file_instance = FileUpload(
            id = uuid.uuid4(),
            filename = file.filename,
            upload_time = datetime.now(),
            status = "completed",
        )

        # Add the file to the database
        db.add(file_instance)
        db.commit()
        
        # Read the contents of the file
        contents = await file.read()

        # Convert bytes to string and parse JSON
        data = json.loads(contents)
        # Store the validated sensor data in the database first
        sensor_data_list = []
        for record in data:
            validated_record = SensorDataSchema(**record)
            sensor_data = SensorData(
                id = uuid.uuid4(),
                sensor_id=validated_record.sensor_id,
                value=validated_record.value,
                timestamp=validated_record.timestamp,
                file_upload_id=file_instance.id
            )
            sensor_data_list.append(sensor_data)

        db.add_all(sensor_data_list)
        db.commit()

        # Send the entire batch of sensor data to Celery for anomaly detection
        task_id = process_sensor_data.delay(file_instance.id)
        return {"status": "File processed successfully", "task_id": task_id}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="File is not a valid JSON.")
    
    except ValidationError as e:
        # Pydantic validation error
        raise HTTPException(status_code=400, detail=str(e))
