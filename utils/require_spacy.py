
def require_spacy(test_case):
    """
    Decorator marking a test that requires SpaCy. These tests are skipped when SpaCy isn't installed.
    """
    return unittest.skipUnless(is_spacy_available(), "test requires spacy")(test_case)

