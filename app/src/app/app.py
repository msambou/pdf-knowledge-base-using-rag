from fastapi import FastAPI, UploadFile, File
from app.models.models import TextOutput
from app.models.chunk import DocumentChunk
from app.models.output import EchoResponse
from app.chat import invoke_chat
from pypdf import PdfReader


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

@app.post("/echo")
def echo(file: UploadFile = File(...)):
    reader = PdfReader(file.file)

    chunks = []
    chunk_id = 0

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text() or ""

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