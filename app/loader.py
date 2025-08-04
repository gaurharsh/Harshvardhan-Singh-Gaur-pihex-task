import os
from pathlib import Path

DATA_DIR = Path("../data")

def load_documents():
    documents = []
    for file in DATA_DIR.glob("*.md"):
        with open(file, "r", encoding="utf-8") as f:
            documents.append({"doc": file.name, "content": f.read()})
    return documents