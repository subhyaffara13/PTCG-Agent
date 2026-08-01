
def require_fouroversix(test_case):
    """
    Decorator marking a test that requires fouroversix
    """
    return unittest.skipUnless(is_fouroversix_available(), "test requires fouroversix")(test_case)

