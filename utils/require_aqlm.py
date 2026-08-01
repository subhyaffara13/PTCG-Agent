
def require_aqlm(test_case):
    """
    Decorator marking a test that requires aqlm
    """
    return unittest.skipUnless(is_aqlm_available(), "test requires aqlm")(test_case)

