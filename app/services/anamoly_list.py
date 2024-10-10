from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.models import AnomalyDetection

router = APIRouter()

@router.get("/anomalies/")
async def get_anomalies(db: Session = Depends(get_db)):
    # Retrieve anomalies from the database
    anomalies = db.query(AnomalyDetection).all()
    if not anomalies:
        raise HTTPException(status_code=404, detail="No anomalies found")
    return [{"id": anomaly.id, "description": anomaly.description, "detected_time": anomaly.detected_time} for anomaly in anomalies]
