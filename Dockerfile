# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for video processing and PostgreSQL
RUN apt-get update && \
    apt-get install -y libpq-dev build-essential ffmpeg ccextractor && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port and run Gunicorn
EXPOSE 8000
CMD ["gunicorn", "video_transcribe.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
