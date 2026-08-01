
def require_torch_optimi(test_case):
    """
    Decorator marking a test that requires torch-optimi. These tests are skipped when torch-optimi isn't installed.
    https://github.com/jxnl/torch-optimi
    """
    return unittest.skipUnless(is_torch_optimi_available(), "test requires torch-optimi")(test_case)

