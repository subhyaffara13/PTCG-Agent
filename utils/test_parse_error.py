
def test_parse_error(testcase: DataDrivenTestCase) -> None:
    try:
        options = parse_options("\n".join(testcase.input), testcase, 0)
        if options.python_version < defaults.PYTHON3_VERSION:
            options.python_version = defaults.PYTHON3_VERSION
        if options.python_version != sys.version_info[:2]:
            skip()
        # Compile temporary file. The test file contains non-ASCII characters.
        errors = Errors(options)
        parse(
            bytes("\n".join(testcase.input), "utf-8"),
            INPUT_FILE_NAME,
            "__main__",
            errors=errors,
            options=options,
            eager=True,
        )
        if errors.is_errors():
            errors.raise_error()
        raise AssertionError("No errors reported")
    except CompileError as e:
        if e.module_with_blocker is not None:
            assert e.module_with_blocker == "__main__"
        # Verify that there was a compile error and that the error messages
        # are equivalent.
        assert_string_arrays_equal(
            testcase.output,
            e.messages,
            f"Invalid compiler output ({testcase.file}, line {testcase.line})",
        )

