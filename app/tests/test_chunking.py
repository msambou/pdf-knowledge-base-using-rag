from app.services.chunking import chunk_text # type: ignore

def test_chunk_text_overlap():
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text(text, chunk_size=10, overlap=5)

    assert chunks[0] == "abcdefghij"
    assert chunks[1] == "fghijklmno"
