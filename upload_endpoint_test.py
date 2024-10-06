from fastapi.testclient import TestClient
import json

from app.main import app

client = TestClient(app)

def test_upload_file():
    # Create sample JSON content to upload
    data = [
        {"sensor_id": "sensor_001", "value": 23.5, "timestamp": "2024-10-04T08:30:00"},
        {"sensor_id": "sensor_002", "value": 45.2, "timestamp": "2024-10-04T09:15:00"}
    ]
    json_file = json.dumps(data)
    
    # Send POST request with file upload
    response = client.post("/upload/", files={"file": ("sensor_data.json", json_file, "application/json")})
    
    assert response.status_code == 200
    assert response.json() == {"status": "File processed successfully", "records": 2}
