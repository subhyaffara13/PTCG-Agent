
def assert_string_arrays_equal(
    expected: list[str],
    actual: list[str],
    msg: str,
    *,
    traceback: bool = False,
    ignore_modules_order: bool = False,
) -> None:
    """Assert that two string arrays are equal.

    Display any differences in a human-readable form.
    """
    actual = clean_up(actual)
    if ignore_modules_order:
        expected_module_order = module_order(expected)
        actual = match_module_order(actual, expected_module_order)
    if expected != actual:
        expected_ranges, actual_ranges = diff_ranges(expected, actual)
        sys.stderr.write("Expected:\n")
        red = "\033[31m" if sys.platform != "win32" else None
        render_diff_range(expected_ranges, expected, colour=red)
        sys.stderr.write("Actual:\n")
        green = "\033[32m" if sys.platform != "win32" else None
        render_diff_range(actual_ranges, actual, colour=green)

        sys.stderr.write("\n")
        first_diff = next(
            (i for i, (a, b) in enumerate(zip(expected, actual)) if a != b),
            max(len(expected), len(actual)),
        )
        if 0 <= first_diff < len(actual) and (
            len(expected[first_diff]) >= MIN_LINE_LENGTH_FOR_ALIGNMENT
            or len(actual[first_diff]) >= MIN_LINE_LENGTH_FOR_ALIGNMENT
        ):
            # Display message that helps visualize the differences between two
            # long lines.
            show_align_message(expected[first_diff], actual[first_diff])

        sys.stderr.write(
            "Update the test output using --update-data "
            "(implies -n0; you can additionally use the -k selector to update only specific tests)\n"
        )
        pytest.fail(msg, pytrace=traceback)

