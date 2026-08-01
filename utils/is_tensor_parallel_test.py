
def is_tensor_parallel_test(test_case):
    """
    Decorator marking a test as a tensor parallel test. If RUN_TENSOR_PARALLEL_TESTS is set to a falsy value, those
    tests will be skipped.
    """
    if not _run_tensor_parallel_tests:
        return unittest.skip(reason="test is tensor parallel test")(test_case)
    else:
        try:
            import pytest  # We don't need a hard dependency on pytest in the main library
        except ImportError:
            return test_case
        else:
            return pytest.mark.is_tensor_parallel_test()(test_case)

