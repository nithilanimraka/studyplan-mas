# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Serper API key ([Get one here](https://serper.dev/))

## Installation

### Option 1: Automated Setup (macOS/Linux)

```bash
# Run the setup script
./setup.sh
```

### Option 2: Manual Setup

1. **Create virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=sk-your-openai-api-key-here
SERPER_API_KEY=your-serper-api-key-here
```

## Running the Application

```bash
streamlit run streamlit_app/app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### 1. Upload Assignment 📤

- Upload PDF files or paste assignment text
- The system will automatically extract and index the content
- Multiple PDFs can be uploaded

### 2. Generate Study Plan 📅

- Set your assignment deadline (date and time)
- Click "Generate Study Plan"
- Wait while AI agents:
  - Extract assignment details
  - Research relevant resources
  - Create a personalized study plan

### 3. Chat with Assignment 💬

- Ask questions about your assignment
- Get answers from your documents + web research
- All responses include source citations

## Features

- **Automatic Detail Extraction**: GPT-4o analyzes your assignment
- **Web Research**: SerperAPI finds the best learning resources
- **Personalized Planning**: AI creates a detailed study schedule
- **RAG Q&A**: Ask questions about uploaded materials
- **Web-Enhanced Answers**: Every response includes web research

## Architecture

### Agents
1. **Assignment Analyzer** - Extracts key details from documents
2. **Web Research Specialist** - Finds quality learning resources
3. **Study Plan Architect** - Creates detailed study schedules
4. **Enhanced Q&A Assistant** - Answers questions using RAG + web search

### Technology Stack
- **CrewAI**: Multi-agent orchestration
- **OpenAI GPT-4o**: Language model
- **SerperAPI**: Web search
- **ChromaDB**: Vector database
- **Streamlit**: User interface
- **PyPDF**: PDF processing
- **LangChain**: RAG implementation

## Troubleshooting

### API Key Errors

If you see "OPENAI_API_KEY is not set":
```bash
# Check your .env file exists
ls -la .env

# Verify API keys are set (without quotes)
cat .env
```

### Import Errors

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### ChromaDB Issues

```bash
# Clear vector store
rm -rf data/vectorstore/*
```

## API Costs

### OpenAI GPT-4o
- Input: ~$2.50 per 1M tokens
- Output: ~$10.00 per 1M tokens

### SerperAPI
- Free tier: 2,500 searches/month
- Additional: $0.003 per search

**Estimated cost per study plan**: $0.05 - $0.15

## Support

For issues or questions:
1. Check the logs in the terminal
2. Verify API keys are correct
3. Ensure all dependencies are installed
4. Check internet connection for web search

## Project Structure

```
assignment_study_mas/
├── config/              # Configuration and settings
├── data/               # Data storage
│   ├── uploads/        # Uploaded PDFs
│   ├── vectorstore/    # ChromaDB storage
│   └── outputs/        # Generated plans
├── src/
│   ├── agents/         # CrewAI agents
│   ├── crews/          # Crew orchestration
│   ├── tools/          # Custom tools
│   └── utils/          # Utilities
├── streamlit_app/      # Streamlit UI
└── requirements.txt    # Dependencies
```
