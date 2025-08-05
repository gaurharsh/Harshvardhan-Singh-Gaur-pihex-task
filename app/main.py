from fastapi import FastAPI, HTTPException # Import FastAPI framework
from pydantic import BaseModel  # Import Pydantic model base for request validation
from qa_engine import answer_question  # Import the main function that handles QA logic
from schema_validator import validate_schema  # Import the function that validates responses against the JSON schema

# Initialize a FastAPI app instance
app = FastAPI()

# Define the expected request body using Pydantic
class QuestionRequest(BaseModel):
    question: str

# Define a POST API endpoint at '/ask'
@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        # Pass the user's question to the answer engine
        result = answer_question(request.question)

        # Validate the result against the answer_schema.json
        validate_schema(result)

         # If valid, return the result as the API response
        return result
    except Exception as e:

          # If anything fails (e.g., schema mismatch), raise a 422 error
        raise HTTPException(status_code=422, detail=str(e))