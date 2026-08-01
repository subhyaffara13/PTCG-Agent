
def require_clearml(test_case):
    """
    Decorator marking a test requires clearml.

    These tests are skipped when clearml isn't installed.

    """
    return unittest.skipUnless(is_clearml_available(), "test requires clearml")(test_case)

