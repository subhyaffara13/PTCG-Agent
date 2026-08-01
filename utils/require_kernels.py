
def require_kernels(test_case):
    """
    Decorator marking a test that requires the kernels library.

    These tests are skipped when the kernels library isn't installed.

    """
    return unittest.skipUnless(is_kernels_available(), "test requires the kernels library")(test_case)

