from pydantic import BaseModel
from typing import List

class QueryResult(BaseModel):
    text: str
    source: str
    page: int
    chunk_id: int
