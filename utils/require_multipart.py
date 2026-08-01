
def require_multipart(test_case):
    """
    Decorator marking a test that requires python-multipart
    """
    return unittest.skipUnless(is_multipart_available(), "test requires python-multipart")(test_case)

