 Short Explanation of the Code & Process (Ideal for Interviews)
“I built a schema-conforming Question-Answering API over markdown documents using FastAPI and scikit-learn. It accepts user questions via a /ask endpoint, retrieves the most relevant content using TF-IDF + cosine similarity, and returns a structured JSON response containing the answer, confidence score, category, and sources, strictly validated against a given JSON schema.”
 How it works:
1.	Load Markdown Files: All .md docs are loaded from a folder using loader.py.
2.	Chunking: Each document is split into sentences/paragraphs (excluding headings).
3.	Vectorization: All chunks are encoded using TfidfVectorizer.
4.	Similarity Matching: For any incoming question, cosine similarity is used to find the most relevant chunk.
5.	Answer Construction: The best-matching chunk is returned as the answer, along with its source document and snippet.
6.	Schema Validation: Output is passed through jsonschema.validate() to ensure compliance with answer_schema.json.
7.	API Endpoint: Exposed via FastAPI as /ask, accepting JSON questions.
________________________________________



 Sample Output
Input:
{
    "question": "We need data residency in India. Is that available?"
}




Output:
{
    "answer": "- Regional data residency: `in` (India) and `eu` (Frankfurt) regions.",
    "category": "security",
    "confidence": 0.454,
    "sources": [
        {
            "doc": "policy_security.md",
            "snippet": "- Regional data residency: `in` (India) and `eu` (Frankfurt) regions."
        }
    ]
}
 Optional Bonus Points
If you want to show deeper thought:
•	Add an eval.py script that loops over eval_questions.jsonl and scores accuracy.
•	Mention trade-offs in NOTES.md: fast, interpretable, offline-compatible.
________________________________________
app/main.py
•	Defines the FastAPI app and exposes the POST /ask endpoint.
•	Accepts a JSON payload with a "question" field.
•	Delegates answering logic to qa_engine.answer_question().
•	Validates the response against the required schema before returning it.
________________________________________
 app/qa_engine.py
•	Loads .md documents and splits them into meaningful text chunks.
•	Converts both questions and text chunks to TF-IDF vectors using scikit-learn.
•	Finds the best-matching chunk via cosine similarity to form the answer.
•	Returns a response with answer, category, confidence, and sources, adhering strictly to the JSON schema.
________________________________________
 app/loader.py
•	Loads all markdown (.md) files from the data/ folder.
•	Returns a list of documents with filename and full content.
•	Keeps file I/O modular and reusable.
________________________________________
 app/schema_validator.py
•	Loads the answer_schema.json from the data/ directory.
•	Validates any outgoing API response to ensure it conforms to the schema.
•	Uses the jsonschema library for compliance enforcement.
________________________________________
 data/*.md
•	Markdown files serve as the knowledge base for the QA system.
•	Each file contains information related to API policy, pricing, security, FAQs, etc.
•	These are the only sources the system retrieves answers from.
________________________________________
 data/eval_questions.jsonl
•	Contains test queries to evaluate if the system gives expected answers.
•	Each test includes a question, expected category, and key terms expected in the answer.
________________________________________
 data/answer_schema.json
•	Defines the required structure of the response JSON:
o	answer: string
o	category: one of [api, security, pricing, support, other]
o	confidence: number between 0–1
o	sources: list of objects with doc and optional snippet
________________________________________
 requirements.txt
•	Lists required Python libraries: fastapi, uvicorn, scikit-learn, jsonschema, etc.
•	Used to set up the project environment quickly via pip install -r requirements.txt.
________________________________________
 README.md
•	Explains how to run the app locally:
o	Install dependencies
o	Start server using Uvicorn
o	How to test the /ask endpoint with sample payload
________________________________________
 NOTES.md
•	Documents the architecture decisions and trade-offs.
•	Mentions why TF-IDF was used and how the system could be improved (e.g., embeddings, LLMs).
________________________________________

