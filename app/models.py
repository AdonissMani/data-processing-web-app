from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres import Base
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

class FileUpload(Base):
    __tablename__ = "file_uploads"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    filename = Column(String, index=True)
    upload_time = Column(DateTime, default=datetime.now)
    status = Column(String, default="pending")

    # One-to-many relationship with SensorData
    sensor_data = relationship("SensorData", back_populates="file_upload")

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    sensor_id = Column(String, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    # Foreign key to FileUpload
    file_upload_id = Column(UUID(as_uuid=True), ForeignKey("file_uploads.id"))

    # Relationships
    file_upload = relationship("FileUpload", back_populates="sensor_data")
    anomalies = relationship("AnomalyDetection", back_populates="sensor_data")

class AnomalyDetection(Base):
    __tablename__ = "anomalies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    description = Column(String)
    sensor_data_id = Column(UUID(as_uuid=True), ForeignKey("sensor_data.id"))
    detected_time = Column(DateTime, default=datetime.now)

    # Relationship back to SensorData
    sensor_data = relationship("SensorData", back_populates="anomalies")
