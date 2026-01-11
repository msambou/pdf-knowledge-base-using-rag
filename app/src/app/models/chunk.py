from pydantic import BaseModel

class DocumentChunk(BaseModel):
    text: str
    source: str        # filename
    page: int
    chunk_id: int