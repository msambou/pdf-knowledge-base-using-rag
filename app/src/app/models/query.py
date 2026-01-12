from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    question: str
    k: int = 5

class QueryResult(BaseModel):
    text: str
    source: str
    page: int
    chunk_id: int

class QueryResponse(BaseModel):
    answer: str
    sources: list[QueryResult]