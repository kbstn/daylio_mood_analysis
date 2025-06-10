# Daylio Mood Analysis

A personal analytics platform for mood and health data, providing insights into patterns and correlations.

## ✨ Features

- **Unified Data Hub**: Centralize mood, weight, and activity data
- **Privacy-First**: Local data processing with optional cloud sync
- **Actionable Insights**: Identify correlations and trends
- **Modular Design**: Easy to extend with new data sources

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- UV (https://astral.sh/uv/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/daylio-mood-analysis.git
   cd daylio-mood-analysis
   ```

2. **Set up UV environment**
   ```bash
   # Install UV if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies
   uv pip install -e ".[dev]"
   ```

3. **Run the application**
   ```bash
   # Start the Streamlit app
   streamlit run app/ui/dashboard.py
   ```

## 🏗️ Project Structure

```
daylio_mood_analysis/
├── app/                # Application code
│   ├── core/          # Business logic and models
│   ├── db/            # Database layer
│   ├── processing/    # Data processing
│   └── ui/            # Streamlit components
├── tests/             # Test suite
├── scripts/           # Utility scripts
└── data/              # Data and migrations
```

## 🛠️ Development

### Code Quality
```bash
# Run formatters
black .
isort .

# Run type checking
mypy .

# Run tests
pytest
```

### Pre-commit Hooks
```bash
pre-commit install
pre-commit run --all-files
```

## 📝 License

MIT
