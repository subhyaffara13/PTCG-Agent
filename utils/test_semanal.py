
def test_semanal(testcase: DataDrivenTestCase) -> None:
    """Perform a semantic analysis test case.

    The testcase argument contains a description of the test case
    (inputs and output).
    """

    try:
        src = "\n".join(testcase.input)
        options = get_semanal_options(src, testcase)
        options.python_version = testfile_pyversion(testcase.file)
        result = build.build(
            sources=[BuildSource("main", None, src)], options=options, alt_lib_path=test_temp_dir
        )
        a = result.errors
        if a:
            raise CompileError(a)
        # Include string representations of the source files in the actual
        # output.
        for module in sorted(result.files.keys()):
            if module in testcase.test_modules:
                a += result.files[module].str_with_options(options).split("\n")
    except CompileError as e:
        a = e.messages
    if testcase.normalize_output:
        a = normalize_error_messages(a)
    assert_string_arrays_equal(
        testcase.output,
        a,
        f"Invalid semantic analyzer output ({testcase.file}, line {testcase.line})",
    )

