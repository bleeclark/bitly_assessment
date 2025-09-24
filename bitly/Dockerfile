# Bitly Backend Engineer Coding Challenge - Dockerfile
# 
# This Dockerfile creates a containerized environment for running the click counter solution.
# It uses Python 3.11 slim image for optimal size and performance.

FROM python:3.11-slim

# Set metadata
LABEL maintainer="Bitly Coding Challenge"
LABEL description="Containerized solution for Bitly Backend Engineer Coding Challenge"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (minimal, since we only use standard library)
# No additional packages needed as solution uses only Python standard library
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY click_counter.py .
COPY test_click_counter.py .
COPY requirements.txt .

# Create directory for data files
RUN mkdir -p /app/data

# Copy sample data files (if they exist)
COPY encodes.csv data/ 2>/dev/null || echo "Sample encodes.csv not found, will use user-provided file"
COPY decodes.json data/ 2>/dev/null || echo "Sample decodes.json not found, will use user-provided file"

# Set default command to run the click counter
CMD ["python", "click_counter.py"]

# Instructions for using this Dockerfile:
# 
# 1. Build the image:
#    docker build -t bitly-click-counter .
#
# 2. Run with your data files:
#    docker run -v /path/to/your/data:/app/data bitly-click-counter
#
# 3. Run tests:
#    docker run bitly-click-counter python test_click_counter.py
#
# 4. Interactive shell:
#    docker run -it bitly-click-counter /bin/bash
