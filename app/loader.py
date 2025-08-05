# Import modules to work with file paths
import os
from pathlib import Path

# Set the path to the 'data' directory (relative to project root)
DATA_DIR = Path("../data")
# Function to load all .md files from the data directory
def load_documents():
    documents = []
     # Loop through each markdown file in the data folder
    for file in DATA_DIR.glob("*.md"):
        # Open the file and read its content
        with open(file, "r", encoding="utf-8") as f:
            documents.append({"doc": file.name, "content": f.read()}) 
    return documents   # Return a list of dicts, each containing doc name and content