from loader import load_documents
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DOCUMENTS = load_documents()

# Split documents into sentence-level chunks
def extract_chunks(doc_text):
    lines = doc_text.splitlines()
    chunks = []
    for i, line in enumerate(lines):
        if line.strip() and not line.strip().startswith("#"):
            chunks.append(line.strip())
    return chunks

# Build passage-level index
passages = []
passage_map = []
for doc in DOCUMENTS:
    chunks = extract_chunks(doc["content"])
    for chunk in chunks:
        passages.append(chunk)
        passage_map.append({"doc": doc["doc"], "chunk": chunk})

vectorizer = TfidfVectorizer().fit(passages)
X = vectorizer.transform(passages)

def answer_question(question):
    q_vec = vectorizer.transform([question])
    similarities = cosine_similarity(q_vec, X).flatten()
    top_idx = int(np.argmax(similarities))
    top_score = round(float(similarities[top_idx]), 3)

    best_passage = passage_map[top_idx]
    answer_text = best_passage["chunk"]
    source_doc = best_passage["doc"]

    # Category classification
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

    return {
        "answer": answer_text,
        "category": category,
        "confidence": min(top_score, 1.0),
        "sources": [
            {
                "doc": source_doc,
                "snippet": answer_text[:200]
            }
        ]
    }
