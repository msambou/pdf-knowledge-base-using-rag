from app.services.embeddings import EmbeddingService

def test_embedding_shape():
    service = EmbeddingService()
    embeddings = service.embed_texts(["hello", "world"])

    assert embeddings.shape[0] == 2
    assert embeddings.shape[1] > 100
