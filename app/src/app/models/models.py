
from pydantic import BaseModel

class TextOutput(BaseModel):
    text: str
    length: int

