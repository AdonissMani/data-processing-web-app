from datetime import datetime
import uuid
from celery import Celery
import os
import logging
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.postgres import SessionLocal  # Correct import for managing session
from app.models import AnomalyDetection, SensorData

logging.basicConfig(level=logging.INFO)

# Celery configuration
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',  # Redis as broker
    backend='redis://redis:6379/0'  # Redis as backend
)

celery_app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

class AnamalyDetectionSchema(BaseModel):
    sensor_id: str
    description: str
    detected_time: datetime

# Example Celery task for processing sensor data
@celery_app.task
def process_sensor_data(file_upload_id: uuid.UUID):
    # database session
    db = SessionLocal()  # Create a new session

    try:
        # Anomaly detection logic
        logging.info("========== Processing sensor data ==========")
        sensor_data = db.query(SensorData).filter(SensorData.file_upload_id == file_upload_id)
        anomalies = []
        for record in sensor_data:
            if record.value > 100:  # Threshold for anomaly detection
                logging.info(f"Anomaly detected for sensor {record.id}")
                
                # Store anomaly in database
                anomaly = AnomalyDetection(
                    id = uuid.uuid4(),
                    sensor_data_id=record.id,
                    description=f"Value exceeds threshold of 100 : {record.value}",
                    detected_time=datetime.now()
                )
                anomalies.append(anomaly)

        db.add_all(anomalies)
        db.commit()  # Commit the changes to the database
        logging.info("========== Anomaly detection completed ==========")

    except Exception as e:
        logging.error(f"Error while processing sensor data: {e}")
        db.rollback()  # Rollback in case of error
    finally:
        db.close() 