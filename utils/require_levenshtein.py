
def require_levenshtein(test_case):
    """
    Decorator marking a test that requires Levenshtein.

    These tests are skipped when Levenshtein isn't installed.

    """
    return unittest.skipUnless(is_levenshtein_available(), "test requires Levenshtein")(test_case)

