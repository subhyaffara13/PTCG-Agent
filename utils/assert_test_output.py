
def assert_test_output(
    testcase: DataDrivenTestCase,
    actual: list[str],
    message: str,
    expected: list[str] | None = None,
    formatted: list[str] | None = None,
) -> None:
    __tracebackhide__ = True

    expected_output = expected if expected is not None else testcase.output
    if expected_output != actual and testcase.config.getoption("--update-data", False):
        update_testcase_output(testcase, actual)

    assert_string_arrays_equal(
        expected_output, actual, f"{message} ({testcase.file}, line {testcase.line})"
    )

