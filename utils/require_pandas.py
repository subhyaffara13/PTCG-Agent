
def require_pandas(test_case):
    """
    Decorator marking a test that requires pandas. These tests are skipped when pandas isn't installed.
    """
    return unittest.skipUnless(is_pandas_available(), "test requires pandas")(test_case)

