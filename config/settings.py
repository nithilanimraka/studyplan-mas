"""Application settings and configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"
OUTPUTS_DIR = DATA_DIR / "outputs"

# Create directories if they don't exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Model Configuration
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Vector Database
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(VECTORSTORE_DIR))

# App Settings
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Validate required API keys
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in .env file")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY is not set in .env file")
