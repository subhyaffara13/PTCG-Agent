
def require_seqio(test_case):
    """
    Decorator marking a test that requires SentencePiece. These tests are skipped when SentencePiece isn't installed.
    """
    return unittest.skipUnless(is_seqio_available(), "test requires Seqio")(test_case)

