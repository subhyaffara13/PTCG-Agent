
def is_training_test(test_case):
    """
    Decorator marking a test as a training test. If RUN_TRAINING_TESTS is set to a falsy value, those tests will be
    skipped.
    """
    if not _run_training_tests:
        return unittest.skip(reason="test is training test")(test_case)
    else:
        try:
            import pytest  # We don't need a hard dependency on pytest in the main library
        except ImportError:
            return test_case
        else:
            return pytest.mark.is_training_test()(test_case)

