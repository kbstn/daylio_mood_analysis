# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port that will be provided at runtime
ENV STREAMLIT_SERVER_PORT=${STREAMLIT_SERVER_PORT}
EXPOSE ${STREAMLIT_SERVER_PORT}

# Command to run the application (using shell form for env var expansion)
CMD streamlit run app.py --server.port=${STREAMLIT_SERVER_PORT} --server.address=0.0.0.0