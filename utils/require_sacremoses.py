
def require_sacremoses(test_case):
    """
    Decorator marking a test that requires Sacremoses. These tests are skipped when Sacremoses isn't installed.
    """
    return unittest.skipUnless(is_sacremoses_available(), "test requires Sacremoses")(test_case)

