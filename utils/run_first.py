
def run_first(test_case):
    """
    Decorator marking a test with order(1). When pytest-order plugin is installed, tests marked with this decorator
    are guaranteed to run first.

    This is especially useful in some test settings like on a Gaudi instance where a Gaudi device can only be used by a
    single process at a time. So we make sure all tests that run in a subprocess are launched first, to avoid device
    allocation conflicts.
    """
    # Without this check, we get unwanted warnings when it's not installed
    if is_pytest_order_available():
        import pytest

        return pytest.mark.order(1)(test_case)
    else:
        return test_case

