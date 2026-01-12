
from pydantic import BaseModel
from .query_result import QueryResult

class QueryResponse(BaseModel):
    answer: str
    sources: list[QueryResult]
