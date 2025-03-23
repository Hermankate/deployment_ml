import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

# Database configuration
DATABASE_NAME = "resumes.db"
DATABASE_PATH = BASE_DIR / DATABASE_NAME

# Hugging Face settings
HF_API_KEY = os.getenv("HF_API_KEY")
LLAMA_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Feature engineering
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 2)

# Thresholds
DEFAULT_GOOD_FIT = 0.7
DEFAULT_POTENTIAL_FIT = 0.4