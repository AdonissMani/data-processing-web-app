# Use an official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app/app

# Copy the requirements and install dependencies
COPY Pipfile* /app/
RUN pip install pipenv && pipenv install --system --deploy

# Copy the application code
COPY app /app/app

# Expose the FastAPI port
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
