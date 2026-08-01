
def require_ipython(test_case):
    """Decorator marking a test that requires IPython. These tests are skipped when IPython isn't installed."""
    return unittest.skipUnless(is_ipython_available(), "test requires `IPython`")(test_case)

