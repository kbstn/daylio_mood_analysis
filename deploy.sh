#!/bin/bash

# Exit on error
set -e

# Set project directory
PROJECT_DIR="/opt/containers/daylio_mood_analysis"

# Create directory if it doesn't exist
sudo mkdir -p /opt/containers

# Navigate to containers directory
cd /opt/containers/

# Remove existing directory if it exists
if [ -d "$PROJECT_DIR" ]; then
    echo "Removing existing project directory..."
    sudo rm -rf "$PROJECT_DIR"
fi

# Clone the repository
echo "Cloning repository..."
sudo git clone https://github.com/kbstn/daylio_mood_analysis.git

# Navigate to project directory
cd "$PROJECT_DIR"

# Copy example.env to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    sudo cp example.env .env
    
    # Set default values from example.env if they exist
    DEFAULT_PORT=$(grep -E '^STREAMLIT_SERVER_PORT=' example.env | cut -d '=' -f2- || echo "8508")
    DEFAULT_ADDRESS=$(grep -E '^STREAMLIT_SERVER_ADDRESS=' example.env | cut -d '=' -f2- || echo "0.0.0.0")
    DEFAULT_TRAEFIK_HOST=$(grep -E '^TRAEFIK_HOST=' example.env | cut -d '=' -f2- || echo "your-domain.example.com")
    
    # Prompt user for values
    read -p "Enter Streamlit server port [$DEFAULT_PORT]: " PORT
    PORT=${PORT:-$DEFAULT_PORT}
    
    read -p "Enter Streamlit server address [$DEFAULT_ADDRESS]: " ADDRESS
    ADDRESS=${ADDRESS:-$DEFAULT_ADDRESS}
    
    read -p "Enter Traefik host [$DEFAULT_TRAEFIK_HOST]: " TRAEFIK_HOST
    TRAEFIK_HOST=${TRAEFIK_HOST:-$DEFAULT_TRAEFIK_HOST}
    
    # Update .env file with user values
    sudo sh -c "cat > .env << EOL
# Application settings
STREAMLIT_SERVER_PORT=$PORT
STREAMLIT_SERVER_ADDRESS=$ADDRESS

# Traefik settings - update with your domain for deploying it in traefik environment
TRAEFIK_HOST=$TRAEFIK_HOST
EOL"
    
    echo ".env file has been configured with your settings."
fi

# Build and start the containers
echo "Starting Docker Compose..."
sudo docker compose up -d --build

echo -e "\nContainer is starting up..."
echo "Streamlit dashboard will be available at http://localhost:$PORT"

# Show logs
echo -e "\nShowing logs (press Ctrl+C to exit):"
sudo docker compose logs -f
