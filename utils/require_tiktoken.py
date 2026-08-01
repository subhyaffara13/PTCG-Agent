
def require_tiktoken(test_case):
    """
    Decorator marking a test that requires TikToken. These tests are skipped when TikToken isn't installed.
    """
    return unittest.skipUnless(is_tiktoken_available(), "test requires TikToken")(test_case)

