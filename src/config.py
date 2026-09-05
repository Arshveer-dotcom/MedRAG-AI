import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

USE_OPENAI = bool(OPENAI_API_KEY)

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

CHROMA_PERSIST_DIRECTORY_STR = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
CHROMA_PERSIST_DIRECTORY_PATH = Path(CHROMA_PERSIST_DIRECTORY_STR)
if not CHROMA_PERSIST_DIRECTORY_PATH.is_absolute():
    CHROMA_PERSIST_DIRECTORY = BASE_DIR / CHROMA_PERSIST_DIRECTORY_PATH
else:
    CHROMA_PERSIST_DIRECTORY = CHROMA_PERSIST_DIRECTORY_PATH

CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "medical_documents")

MEDICAL_DOCS_DIR = BASE_DIR / "data" / "medical_documents"

MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", 5))

STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", 8501))
STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")