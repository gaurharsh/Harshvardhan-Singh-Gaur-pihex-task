
#  PiHex QA API

A FastAPI-based Question Answering API over markdown docs.  
Uses scikit-learn TF-IDF to find the most relevant answer.  
Returns structured JSON with category, confidence, and sources.  
Fully validates responses against a given JSON schema.  
Easy to run locally or via Docker.


## Features

- Accepts questions via `POST /ask`
- Extracts answers from `.md` documents using TF-IDF + cosine similarity
- Returns structured responses that strictly follow the provided `answer_schema.json`

---

##  How to Run Locally

1. **Clone this repo**

```bash
git clone <your-repo-url>
cd <project-directory>
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Start the server**

```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

---

##  API Usage

### Endpoint

```
POST /ask
Content-Type: application/json
```

### Request Body

```json
{
  "question": "What are the rate limits on Pro and do 429s include retry hints?"
}
```

### Sample Response

```json
{
  "answer": "Pro: 60 req/min, 200k tokens/day.\n429s include a Retry-After header (seconds).",
  "category": "api",
  "confidence": 0.92,
  "sources": [
    {
      "doc": "policy_api.md",
      "snippet": "Pro: 60 req/min, 200k tokens/day."
    }
  ]
}
```

---

##  Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI server
│   ├── qa_engine.py         # Core question-answering logic
│   ├── loader.py            # Loads .md files
│   └── schema_validator.py  # Validates response against answer_schema
├── data/                    # Knowledge base files + schema
│   ├── *.md                 # Markdown source files
│   ├── answer_schema.json   # Output JSON schema
│   └── eval_questions.jsonl # Evaluation questions
├── requirements.txt         # Dependencies
├── README.md                # You're here
├── NOTES.md                 # Architecture & tradeoffs
└── Dockerfile               # (Optional) containerization
```

---

##  Schema Compliance

This API strictly validates all responses against the JSON Schema defined in `data/answer_schema.json` using the `jsonschema` library.

---

##  Optional: Docker Usage

```bash
docker build -t pihex-qa-api .
docker run -p 8000:8000 pihex-qa-api
```

---

---

Made with ❤️ by Harshvardhan Singh Gaur


```
