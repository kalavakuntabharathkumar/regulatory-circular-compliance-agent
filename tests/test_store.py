from app.store import chunk_text, add_circular, retrieve, clear_store

def setup_function():
    clear_store()

def test_chunk_text_empty():
    assert chunk_text("   ") == []

def test_ingest_and_retrieve():
    result = add_circular("Demo", "RBI", "Customer due diligence records should be reviewed periodically.")
    assert result["chunks_added"] == 1
    matches = retrieve("customer due diligence review")
    assert matches
    assert matches[0][0].title == "Demo"
