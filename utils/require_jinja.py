
def require_jinja(test_case):
    """
    Decorator marking a test that requires jinja. These tests are skipped when jinja isn't installed.
    """
    return unittest.skipUnless(is_jinja_available(), "test requires jinja")(test_case)

