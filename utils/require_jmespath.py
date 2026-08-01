
def require_jmespath(test_case):
    """
    Decorator marking a test that requires jmespath. These tests are skipped when jmespath isn't installed.
    """
    return unittest.skipUnless(is_jmespath_available(), "test requires jmespath")(test_case)

