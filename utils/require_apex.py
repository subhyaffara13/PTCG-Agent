
def require_apex(test_case):
    """
    Decorator marking a test that requires apex
    """
    return unittest.skipUnless(is_apex_available(), "test requires apex")(test_case)

