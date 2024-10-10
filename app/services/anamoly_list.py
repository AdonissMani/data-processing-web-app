from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.models import AnomalyDetection

router = APIRouter()

@router.get("/anomalies/")
async def get_anomalies(db: Session = Depends(get_db)):
    """
    Retrieves a list of all anomalies from the database.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the id, description and detected_time of an anomaly.
    Raises:
        HTTPException: If no anomalies are found in the database.
    """
    # Retrieve anomalies from the database
    anomalies = db.query(AnomalyDetection).all()
    if not anomalies:
        raise HTTPException(status_code=404, detail="No anomalies found")
    # Return a list of dictionaries, each containing the id, description and detected_time of an anomaly
    return [{"id": anomaly.id, "description": anomaly.description, "detected_time": anomaly.detected_time} for anomaly in anomalies]
