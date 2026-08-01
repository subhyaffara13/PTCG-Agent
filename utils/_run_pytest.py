
def _run_pytest(data_suite: str) -> PytestResult:
    return run_pytest_data_suite(data_suite, extra_args=[], max_attempts=1)

