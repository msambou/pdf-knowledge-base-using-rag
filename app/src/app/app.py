from pypdf import PdfReader # type: ignore
from fastapi import FastAPI, UploadFile, File # type: ignore

from app.models.models import TextOutput
from app.models.chunk import DocumentChunk
from app.models.output import EchoResponse
from app.chat import invoke_chat
from app.services.chunking import chunk_text



app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    text = "Ok"
    return TextOutput(text=text, length=len(text))

@app.get("/chat")
def chat():
    text = "Invoking chat"
    ollama_response = invoke_chat()
    print(ollama_response)
    return TextOutput(text=text, length=len(text))

@app.post("/echo", response_model=EchoResponse)
def echo(file: UploadFile = File(...)):
    reader = PdfReader(file.file)

    chunks = []
    chunk_id = 0

    for page_number, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""

        page_chunks = chunk_text(page_text)

        for text in page_chunks:
            if text.strip():
                chunks.append(
                    DocumentChunk(
                        text=text,
                        source=file.filename,
                        page=page_number + 1,
                        chunk_id=chunk_id,
                    )
                )
                chunk_id += 1

    return EchoResponse(
        filename=file.filename,
        chunks=chunks,
    )