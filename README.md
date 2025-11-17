# Assignment Study Plan - Multi-Agent System

A CrewAI-powered multi-agent application that generates personalized study plans and provides intelligent Q&A for course assignments.

## Features

- **PDF & Text Input**: Upload assignment documents or paste text directly
- **Automatic Detail Extraction**: Uses GPT-4o to extract assignment topic, course name, and requirements
- **Web Research**: Automated research agent finds relevant study resources
- **Personalized Study Plans**: AI-generated study plans with weekly breakdowns based on deadline
- **RAG-Powered Q&A**: Chat with your assignment materials
- **Web-Enhanced Answers**: Every query is enhanced with real-time web search

## Setup

1. Clone the repository and navigate to the project directory

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Add your API keys to `.env`:
   - `OPENAI_API_KEY`: Get from https://platform.openai.com/api-keys
   - `SERPER_API_KEY`: Get from https://serper.dev/

## Usage

Run the Streamlit app:
```bash
streamlit run streamlit_app/app.py
```

## Architecture

### Agents
- **Research Agent**: Web research specialist using SerperAPI
- **Planning Agent**: Creates structured study plans
- **RAG Agent**: Answers questions from uploaded documents
- **Web RAG Agent**: Enhances answers with web search

### Tech Stack
- **CrewAI**: Multi-agent orchestration
- **OpenAI GPT-4o**: Language model
- **ChromaDB**: Vector database for RAG
- **SerperAPI**: Web search
- **Streamlit**: User interface
- **PyPDF**: PDF text extraction
