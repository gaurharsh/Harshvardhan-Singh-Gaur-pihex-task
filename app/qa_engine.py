# Load markdown documents from the data folder
from loader import load_documents
# Import scikit-learn tools for TF-IDF and similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# NumPy for array operations
import numpy as np
# Load all markdown documents at startup
DOCUMENTS = load_documents()

# Split documents into sentence-level chunks
def extract_chunks(doc_text):
    lines = doc_text.splitlines()
    chunks = []
    for i, line in enumerate(lines):
        # Ignore headings and blank lines
        if line.strip() and not line.strip().startswith("#"):
            chunks.append(line.strip())
    return chunks

# Create lists to store all individual text chunks (passages) and their metadata
passages = []
passage_map = []
# Go through each document and extract its content into chunks
for doc in DOCUMENTS:
    chunks = extract_chunks(doc["content"])
    for chunk in chunks:
        passages.append(chunk)
        passage_map.append({"doc": doc["doc"], "chunk": chunk}) # Keep track of which doc the chunk came from

# Create a TF-IDF vectorizer from all passages
vectorizer = TfidfVectorizer().fit(passages)
X = vectorizer.transform(passages)

# Main function to answer a user's question
def answer_question(question):
      # Convert the user's question into TF-IDF vector
    q_vec = vectorizer.transform([question])

        # Compute cosine similarity between question and all passages
    similarities = cosine_similarity(q_vec, X).flatten()
     # Find the index of the most similar passage
    top_idx = int(np.argmax(similarities))
    top_score = round(float(similarities[top_idx]), 3)
    # Retrieve the best matching passage and its source document

    best_passage = passage_map[top_idx]
    answer_text = best_passage["chunk"]
    source_doc = best_passage["doc"]

    # --- Simple rule-based category classification ---

    lower_q = question.lower()
    if any(k in lower_q for k in ["rate limit", "429", "extract endpoint", "strict_schema"]):
        category = "api"
    elif any(k in lower_q for k in ["pii", "training", "data residency", "region"]):
        category = "security"
    elif any(k in lower_q for k in ["pricing", "overage", "cost", "₹"]):
        category = "pricing"
    elif any(k in lower_q for k in ["snippet", "citation", "references", "return_sources"]):
        category = "support"
    else:
        category = "other"
 # Return the final answer in schema-compliant format
    return {
        "answer": answer_text,
        "category": category,
        "confidence": min(top_score, 1.0),    # Confidence capped at 1.0

        "sources": [
            {
                "doc": source_doc,
                "snippet": answer_text[:200]  # First 200 chars for context snippet
            }
        ]
    }
