from app.ingestion import chunk_text

def test_chunk_text_returns_chunks():
    result = chunk_text("a " * 1200, size=100, overlap=10)
    assert len(result) > 1
    assert all(result)
