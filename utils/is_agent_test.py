
def is_agent_test(test_case):
    """
    Decorator marking a test as an agent test. If RUN_TOOL_TESTS is set to a falsy value, those tests will be skipped.
    """
    if not _run_agent_tests:
        return unittest.skip(reason="test is an agent test")(test_case)
    else:
        try:
            import pytest  # We don't need a hard dependency on pytest in the main library
        except ImportError:
            return test_case
        else:
            return pytest.mark.is_agent_test()(test_case)

