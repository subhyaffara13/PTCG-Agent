
def require_torchcodec(test_case):
    """
    Decorator marking a test that requires Torchcodec.

    These tests are skipped when Torchcodec isn't installed.

    """
    return unittest.skipUnless(is_torchcodec_available(), "test requires Torchcodec")(test_case)

