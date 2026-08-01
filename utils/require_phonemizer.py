
def require_phonemizer(test_case):
    """
    Decorator marking a test that requires phonemizer
    """
    return unittest.skipUnless(is_phonemizer_available(), "test requires phonemizer")(test_case)

