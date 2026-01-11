from pydantic import BaseModel
from typing import List
from .chunk import DocumentChunk

class EchoResponse(BaseModel):
    filename: str
    chunks: List[DocumentChunk]
