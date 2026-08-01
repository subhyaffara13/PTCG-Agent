
def require_trackio(test_case):
    """
    Decorator marking a test that requires trackio.

    These tests are skipped when trackio isn't installed.

    """
    return unittest.skipUnless(is_trackio_available(), "test requires trackio")(test_case)

