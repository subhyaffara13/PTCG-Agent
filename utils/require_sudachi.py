
def require_sudachi(test_case):
    """
    Decorator marking a test that requires sudachi
    """
    return unittest.skipUnless(is_sudachi_available(), "test requires sudachi")(test_case)

