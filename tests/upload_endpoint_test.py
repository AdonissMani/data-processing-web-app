import json
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Adjust import according to your structure
from app.models import SensorData
from sqlalchemy.orm import Session
from app.db.postgres import get_db

# Create a test client
client = TestClient(app)

# Dependency override for testing purposes
@pytest.fixture(scope="module")
def override_get_db():
    # Create a new database session for each test
    db = get_db()  # Get your database session here
    yield db
    db.close()  # Close the database session

# Modify the FastAPI app to use the override during testing
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def test_data():
    # Sample JSON content to upload
    return [
        {"sensor_id": "sensor_001", "value": 23.5, "timestamp": "2024-10-04T08:30:00"},
        {"sensor_id": "sensor_002", "value": 45.2, "timestamp": "2024-10-04T09:15:00"}
    ]

def test_upload_file(test_data, override_get_db):  # Use the fixture here
    # Convert sample data to JSON file
    json_file = json.dumps(test_data)
    
    # Send POST request with file upload
    response = client.post(
        "/upload/",
        files={"file": ("sensor_data.json", json_file, "application/json")}
    )
    
    # Assert the response status
    assert response.status_code == 200
    assert response.json() == {"status": "File processed successfully", "task_id": response.json().get("task_id")}
    
    # Verify that the sensor data was saved in the database
    db = override_get_db  # Use the db session from the fixture
    stored_data = db.query(SensorData).all()
    
    assert len(stored_data) == len(test_data)  # Ensure all records were stored
    assert stored_data[0].sensor_id == test_data[0]["sensor_id"]
    assert stored_data[1].sensor_id == test_data[1]["sensor_id"]
