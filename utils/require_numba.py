
def require_numba(test_case):
    """
    Decorator marking a test that requires numba
    """
    return unittest.skipUnless(is_numba_available(), "test requires numba")(test_case)

