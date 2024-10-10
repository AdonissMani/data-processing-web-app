# data-processing-web-app
# Anomaly Detection API

This project provides an API for managing anomaly detections. It includes endpoints for listing anomalies and uploading new anomalies from a JSON file.

## Prerequisites

- Python 3.8+
- PostgreSQL
- `pipenv` (Python package installer)

## Setup

Follow these steps to set up and run the project.

### 1. Clone the repository

```bash
git clone https://github.com/AdonissMani/data-processing-web-app.git
cd data-processing-web-app
```

### 2. Install dependencies
```bash
pipenv install
```

### 3. Activate virtual enviroment
```bash
pipenv shell
```

### 4. Run Services
```bash
sudo docker-compose up --build
```

### 5. Run database migration
```bash
alembic upgrade head
```

### 6. upload endpoint using postman
```
You can use postman collection attached , use sample.json to upload
 http://127.0.0.1:8000 /upload/
```

### 7. List anomaly endpoint using postman
```
 http://127.0.0.1:8000 /anomalies/
```

