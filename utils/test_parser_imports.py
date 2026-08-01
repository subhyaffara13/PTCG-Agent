
def test_parser_imports(testcase: DataDrivenTestCase) -> None:
    """Perform a single native parser imports test case.

    The argument contains the description of the test case.
    This test outputs only reachable import information.
    """
    options = Options()
    options.hide_error_codes = True
    options.python_version = (3, 10)

    source = "\n".join(testcase.input)

    try:
        with temp_source(source) as fnam:
            node, errors, type_ignores = native_parse(fnam, options)
            errors += load_tree(node, options)
            # Extract and format reachable imports
            a = format_reachable_imports(node)
            a = [format_error(err) for err in errors] + a
    except CompileError as e:
        a = e.messages

    assert_string_arrays_equal(
        testcase.output, a, f"Invalid parser output ({testcase.file}, line {testcase.line})"
    )

