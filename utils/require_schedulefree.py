
def require_schedulefree(test_case):
    """
    Decorator marking a test that requires schedulefree. These tests are skipped when schedulefree isn't installed.
    https://github.com/facebookresearch/schedule_free
    """
    return unittest.skipUnless(is_schedulefree_available(), "test requires schedulefree")(test_case)

