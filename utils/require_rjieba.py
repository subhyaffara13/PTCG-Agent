
def require_rjieba(test_case):
    """
    Decorator marking a test that requires rjieba. These tests are skipped when rjieba isn't installed.
    """
    return unittest.skipUnless(is_rjieba_available(), "test requires rjieba")(test_case)

