from pypdf import PdfReader # type: ignore
from fastapi import FastAPI, UploadFile, File # type: ignore

from app.models.models import TextOutput
from app.models.chunk import DocumentChunk
from app.models.output import EchoResponse
from app.services.chunking import chunk_text
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore

from app.models.query import QueryRequest,  QueryResult, QueryResponse

from app.services.prompting import build_prompt
from app.services.llm import LLMService


app = FastAPI()

embedding_service = EmbeddingService()
vector_store = VectorStore(dim=384)

llm_service = LLMService()


@app.get("/healthcheck")
def healthcheck():
    text = "Ok"
    return TextOutput(text=text, length=len(text))

@app.post("/ingest")
def ingest(file: UploadFile = File(...)):
    reader = PdfReader(file.file)

    texts = []
    metadatas = []

    for page_number, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        page_chunks = chunk_text(page_text)

        for i, text in enumerate(page_chunks):
            if text.strip():
                texts.append(text)
                metadatas.append({
                    "text": text,
                    "source": file.filename,
                    "page": page_number + 1,
                    "chunk_id": len(texts) - 1,
                })

    embeddings = embedding_service.embed_texts(texts)
    vector_store.add(embeddings, texts, metadatas)

    return {
        "filename": file.filename,
        "chunks_indexed": len(texts),
    }


@app.post("/query")
def query(request: QueryRequest):
    query_embedding = embedding_service.embed_texts([request.question])
    results = vector_store.search(query_embedding, k=request.k)

    if not results:
        return {
            "answer": "No relevant context found.",
            "sources": [],
        }

    contexts = [r["text"] for r in results]
    prompt = build_prompt(request.question, contexts)
    answer = llm_service.generate(prompt)

    sources = [
        {
            "text": r["metadata"]["text"],
            "source": r["metadata"]["source"],
            "page": r["metadata"]["page"],
            "chunk_id": r["metadata"]["chunk_id"],
        }
        for r in results
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
