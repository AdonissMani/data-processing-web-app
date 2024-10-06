from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import SensorData
from app.db.postgres import get_db
from pydantic import BaseModel, ValidationError
import json

# Create a router instance
router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Example schema definition for the uploaded JSON
class SensorDataSchema(BaseModel):
    sensor_id: str
    value: float
    timestamp: str

# Dependency function to check the file size
def validate_file_size(file: UploadFile):
    if file.spool_max_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 10MB limit.")
    return file

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Ensure the file is a JSON file
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid file format. Only JSON files are allowed.")
    
    try:
        # Read the contents of the file
        contents = await file.read()

        # Convert bytes to string and parse JSON
        data = json.loads(contents)

        # Validate each record in the file
        for record in data:
            validated_record = SensorDataSchema(**record)  # Validating each entry against the Pydantic schema
            sensor_data = SensorData(
                sensor_id = validated_record.sensor_id,
                value = validated_record.value,
                timestamp = validated_record.timestamp
            )
            db.add(sensor_data)
        db.commit()
        # If validation passes, return success response
        return {"status": "File processed successfully", "records": len(data)}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="File is not a valid JSON.")
    
    except ValidationError as e:
        # Pydantic validation error
        raise HTTPException(status_code=400, detail=str(e))
