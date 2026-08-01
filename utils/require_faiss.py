
def require_faiss(test_case):
    """Decorator marking a test that requires faiss."""
    return unittest.skipUnless(is_faiss_available(), "test requires `faiss`")(test_case)

