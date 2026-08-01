
def require_g2p_en(test_case):
    """
    Decorator marking a test that requires g2p_en. These tests are skipped when SentencePiece isn't installed.
    """
    return unittest.skipUnless(is_g2p_en_available(), "test requires g2p_en")(test_case)

