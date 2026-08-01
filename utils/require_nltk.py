
def require_nltk(test_case):
    """
    Decorator marking a test that requires NLTK.

    These tests are skipped when NLTK isn't installed.

    """
    return unittest.skipUnless(is_nltk_available(), "test requires NLTK")(test_case)

