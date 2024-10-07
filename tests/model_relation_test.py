import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.postgres import Base, get_db  # Adjust import according to your structure
from app.models import FileUpload, SensorData, AnomalyDetection
import uuid
from datetime import datetime

# Database setup for tests
@pytest.fixture(scope='module')
def test_db():
    # Create an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    yield session  # This is where the testing happens

    session.close()
    Base.metadata.drop_all(engine)

def test_file_upload_relationship(test_db):
    # Create a FileUpload instance
    file_upload = FileUpload(
        id=uuid.uuid4(),
        filename='test_file.json',
        upload_time=datetime.now(),
        status='completed'
    )
    
    # Create multiple SensorData instances
    sensor_data_1 = SensorData(
        id=uuid.uuid4(),
        sensor_id='sensor_1',
        value=50.0,
        timestamp=datetime.now(),
        file_upload_id=file_upload.id
    )
    
    sensor_data_2 = SensorData(
        id=uuid.uuid4(),
        sensor_id='sensor_2',
        value=75.0,
        timestamp=datetime.now(),
        file_upload_id=file_upload.id
    )
    
    # Add the instances to the test database session
    test_db.add(file_upload)
    test_db.add(sensor_data_1)
    test_db.add(sensor_data_2)
    test_db.commit()

    # Verify the relationships
    assert len(file_upload.sensor_data) == 2  # Should have 2 related SensorData
    assert sensor_data_1.file_upload == file_upload  # Verify back-reference from SensorData
    assert sensor_data_2.file_upload == file_upload  # Verify back-reference from SensorData

def test_anomaly_detection_relationship(test_db):
    # Create SensorData instance
    sensor_data = SensorData(
        id=uuid.uuid4(),
        sensor_id='sensor_3',
        value=120.0,  # Anomalous value
        timestamp=datetime.now(),
        file_upload_id=None  # No need to link to FileUpload for this test
    )

    # Create AnomalyDetection instance
    anomaly = AnomalyDetection(
        id=uuid.uuid4(),
        description='Value exceeds threshold',
        sensor_data_id=sensor_data.id,
        detected_time=datetime.now()
    )

    # Add the instances to the test database session
    test_db.add(sensor_data)
    test_db.add(anomaly)
    test_db.commit()

    # Verify the relationship
    assert anomaly.sensor_data == sensor_data  # Verify back-reference from AnomalyDetection
    assert sensor_data.anomalies[0] == anomaly  # Verify forward-reference to AnomalyDetection
