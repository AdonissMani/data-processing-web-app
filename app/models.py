from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres import Base
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

# class FileUpload(Base):
#     __tablename__ = "file_uploads"
    
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
#     filename = Column(String, index=True)
#     upload_time = Column(DateTime, default=datetime.now)
#     status = Column(String, default="pending")
    
#     # Relationships
#     sensor_data = relationship("SensorData", back_populates="file")
    
class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    sensor_id = Column(String, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

class AnomalyDetection(Base):
    __tablename__ = "anomalies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    description = Column(String)
    sensor_data_id = Column(UUID(as_uuid=True), ForeignKey("sensor_data.id"))
    detected_time = Column(DateTime, default=datetime.now)

    # Relationships
    sensor_data = relationship("SensorData")
