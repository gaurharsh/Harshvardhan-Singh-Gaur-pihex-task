from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qa_engine import answer_question
from schema_validator import validate_schema

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        result = answer_question(request.question)
        validate_schema(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))