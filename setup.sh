#!/bin/bash

# Setup script for Assignment Study Plan Multi-Agent System

echo "🚀 Setting up Assignment Study Plan System..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "1. Copy .env.example to .env:"
echo "   cp .env.example .env"
echo ""
echo "2. Edit .env and add your API keys:"
echo "   - OPENAI_API_KEY (get from https://platform.openai.com/api-keys)"
echo "   - SERPER_API_KEY (get from https://serper.dev/)"
echo ""
echo "3. Run the application:"
echo "   streamlit run streamlit_app/app.py"
echo ""
