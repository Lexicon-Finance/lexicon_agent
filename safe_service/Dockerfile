


# Use Python 3.11 slim image as base

FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the application code
COPY . ./safe_service/

# Set environment variables
ENV PYTHONPATH=/app:/app/safe_service
ENV PORT=8000

# Expose the port
EXPOSE ${PORT}

# Run the application
CMD exec uvicorn safe_service.main:app --host 0.0.0.0 --port ${PORT} 