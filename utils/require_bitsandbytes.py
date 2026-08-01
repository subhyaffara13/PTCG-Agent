
def require_bitsandbytes(test_case):
    """
    Decorator marking a test that requires the bitsandbytes library. Will be skipped when the library or its hard dependency torch is not installed.
    """
    return unittest.skipUnless(is_bitsandbytes_available(), "test requires bitsandbytes")(test_case)

