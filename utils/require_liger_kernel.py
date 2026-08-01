
def require_liger_kernel(test_case):
    """
    Decorator marking a test that requires liger_kernel
    """
    return unittest.skipUnless(is_liger_kernel_available(), "test requires liger_kernel")(test_case)

