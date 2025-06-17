# 📊 Mood Dashboard

An interactive Streamlit dashboard that visualizes and analyzes mood data from Daylio and weight data from OpenScale. The dashboard provides statistical insights into your mood patterns and weight trends over time.

## ✨ Features

- Upload and analyze Daylio mood export data
- Upload and visualize OpenScale weight data
- Interactive charts showing mood and weight trends
- Customizable rolling mean windows for smoothing data
- Z-score analysis to understand mood deviations
- Containerized with Docker for easy deployment

## 🛠️ Prerequisites

- Docker and Docker Compose installed on your system
- Git (for cloning the repository)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/kbstn/daylio_mood_analysis.git
   cd daylio_mood_analysis
   ```

2. **Set up environment variables**
   ```bash
   cp example.env .env
   # Edit .env file if you need to change default settings
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker compose up -d --build
   ```

4. **Access the dashboard**
   - Open your browser and go to: http://localhost:8501

## 📊 Data Analysis Approach

The dashboard uses the following statistical approach to analyze mood data:
- Maps mood categories to numerical values
- Calculates z-scores to measure how many standard deviations each mood entry is from the mean
- Applies a rolling mean to smooth the data and highlight trends
- Provides interactive controls to adjust the analysis window

## ⚙️ Configuration

Edit the `.env` file to customize:
- `STREAMLIT_SERVER_PORT`: Port to run the Streamlit server (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Network interface to bind to (default: 0.0.0.0)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


