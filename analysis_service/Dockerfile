# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/analysis_service

# Set environment variables
ENV PYTHONPATH=/app/analysis_service:/app
ENV PORT=8001

# Expose the port
EXPOSE ${PORT}

# Run the application
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} 