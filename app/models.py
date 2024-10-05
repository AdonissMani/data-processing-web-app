from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres import Base
from datetime import datetime
from uuid import uuid4

class FileUpload(Base):
    __tablename__ = "file_uploads"
    
    id = Column(uuid4, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_time = Column(DateTime, default=datetime.now)
    status = Column(String, default="pending")
    
    # Relationships
    sensor_data = relationship("SensorData", back_populates="file")
    
class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(uuid4, primary_key=True, index=True)
    sensor_id = Column(String, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

class AnomalyDetection(Base):
    __tablename__ = "anomalies"
    
    id = Column(uuid4, primary_key=True, index=True)
    description = Column(String)
    sensor_data_id = Column(Integer, ForeignKey("sensor_data.id"))
    detected_time = Column(DateTime, default=datetime.now)

    # Relationships
    sensor_data = relationship("SensorData")
