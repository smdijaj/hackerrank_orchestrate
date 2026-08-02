from pathlib import Path

# Root directory
ROOT_DIR = Path(__file__).resolve().parents[2]

# Data directories
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"
OUTPUT_DIR = ROOT_DIR / "data" / "output"

# Models directory
MODELS_DIR = ROOT_DIR / "models"

# Docs directory
DOCS_DIR = ROOT_DIR / "docs"