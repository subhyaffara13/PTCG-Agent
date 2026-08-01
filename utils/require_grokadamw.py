
def require_grokadamw(test_case):
    """
    Decorator marking a test that requires GrokAdamW. These tests are skipped when GrokAdamW isn't installed.
    """
    return unittest.skipUnless(is_grokadamw_available(), "test requires GrokAdamW")(test_case)

