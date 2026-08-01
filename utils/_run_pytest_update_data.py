
def _run_pytest_update_data(data_suite: str) -> PytestResult:
    """
    Runs a suite of data test cases through 'pytest --update-data' until either tests pass
    or until a maximum number of attempts (needed for incremental tests).
    """
    return run_pytest_data_suite(data_suite, extra_args=["--update-data"], max_attempts=3)

