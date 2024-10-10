# Use an official Python image
FROM python:3.11-slim

# Set the working directory to /app (the root of your project)
WORKDIR /app/

# Copy the requirements and install dependencies
COPY Pipfile* /app/
RUN pip install pipenv && pipenv install --system --deploy

# Copy the application code to /app
COPY app /app/app
COPY celery_worker.py /app/
COPY alembic /app/alembic
COPY alembic.ini /app/

# Expose the FastAPI port
EXPOSE 8000

# Command to run FastAPI (specifying the correct path to main.py)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
