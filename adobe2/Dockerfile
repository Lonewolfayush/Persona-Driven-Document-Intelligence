FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set up models and dependencies
RUN python setup_models.py

# Create data directory for input documents
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "main.py", "--help"]

# Example usage:
# docker run -v $(pwd)/sample_data:/app/data document-intelligence \
#   python main.py --documents /app/data --persona "PhD Researcher" --job "Literature review"
