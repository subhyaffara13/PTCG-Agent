
def test_semanal_error(testcase: DataDrivenTestCase) -> None:
    """Perform a test case."""

    try:
        src = "\n".join(testcase.input)
        res = build.build(
            sources=[BuildSource("main", None, src)],
            options=get_semanal_options(src, testcase),
            alt_lib_path=test_temp_dir,
        )
        a = res.errors
    except CompileError as e:
        # Verify that there was a compile error and that the error messages
        # are equivalent.
        a = e.messages
    if testcase.normalize_output:
        a = normalize_error_messages(a)
    assert_string_arrays_equal(
        testcase.output, a, f"Invalid compiler output ({testcase.file}, line {testcase.line})"
    )

