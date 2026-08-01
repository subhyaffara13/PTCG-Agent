
def require_cython(test_case):
    """
    Decorator marking a test that requires jumanpp
    """
    return unittest.skipUnless(is_cython_available(), "test requires cython")(test_case)

