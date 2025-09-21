# backend/Dockerfile

# Use an official lightweight Python image for a smaller container
FROM python:3.11-slim

# Set environment variables for best practices
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
# Expose port 8080 (Cloud Run expects this)
EXPOSE 8080

# Run the web server using gunicorn on container startup
# FIX: Changed timeout from 0 (disabled) to 120 seconds to prevent workers from hanging indefinitely.

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 120 main:app
