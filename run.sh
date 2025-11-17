#!/bin/bash

# Run the Streamlit application

echo "🚀 Starting Assignment Study Plan System..."
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env file with your API keys:"
    echo "  cp .env.example .env"
    echo "  Then edit .env to add your OPENAI_API_KEY and SERPER_API_KEY"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Run Streamlit app
echo "📚 Launching Streamlit application..."
streamlit run streamlit_app/app.py
