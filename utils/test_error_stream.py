
def test_error_stream(testcase: DataDrivenTestCase) -> None:
    """Perform a single error streaming test case.

    The argument contains the description of the test case.
    """
    options = Options()
    options.show_traceback = True
    options.hide_error_codes = True

    logged_messages: list[str] = []

    def flush_errors(filename: str | None, msgs: list[str], serious: bool) -> None:
        if msgs:
            logged_messages.append("==== Errors flushed ====")
            logged_messages.extend(msgs)

    sources = [BuildSource("main", "__main__", "\n".join(testcase.input))]
    try:
        build.build(sources=sources, options=options, flush_errors=flush_errors)
    except CompileError as e:
        assert e.messages == []

    assert_string_arrays_equal(
        testcase.output, logged_messages, f"Invalid output ({testcase.file}, line {testcase.line})"
    )

