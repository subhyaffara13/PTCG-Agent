
def require_timm(test_case):
    """
    Decorator marking a test that requires Timm.

    These tests are skipped when Timm isn't installed.

    """
    return unittest.skipUnless(is_timm_available(), "test requires Timm")(test_case)

