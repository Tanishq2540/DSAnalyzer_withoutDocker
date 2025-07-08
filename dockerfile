# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements file to install dependencies first (cache-friendly)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose Streamlit default port
EXPOSE 7860

# Optional: avoid telemetry and CORS issues in deployment
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.enableCORS=false"]
