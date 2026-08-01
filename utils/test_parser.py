
def test_parser():
    assert Abs(parse_maxima('float(1/3)') - 0.333333333) < 10**(-5)
    assert parse_maxima('13^26') == 91733330193268616658399616009
    assert parse_maxima('sin(%pi/2) + cos(%pi/3)') == Rational(3, 2)
    assert parse_maxima('log(%e)') == 1


def test_parser(testcase: DataDrivenTestCase) -> None:
    """Perform a single parser test case.

    The argument contains the description of the test case.
    """
    options = Options()
    options.hide_error_codes = True

    if testcase.file.endswith("python310.test"):
        options.python_version = (3, 10)
    elif testcase.file.endswith("python312.test"):
        options.python_version = (3, 12)
    elif testcase.file.endswith("python313.test"):
        options.python_version = (3, 13)
    elif testcase.file.endswith("python314.test"):
        options.python_version = (3, 14)
    else:
        options.python_version = defaults.PYTHON3_VERSION

    source = "\n".join(testcase.input)

    # Apply mypy: comments to options.
    comments = get_mypy_comments(source)
    changes, _ = parse_mypy_comments(comments, options)
    options = options.apply_changes(changes)

    try:
        errors = Errors(options)
        n = parse(
            bytes(source, "ascii"),
            fnam="main",
            module="__main__",
            errors=errors,
            options=options,
            eager=True,
        )
        if errors.is_errors():
            errors.raise_error()
        a = n.str_with_options(options).split("\n")
    except CompileError as e:
        a = e.messages
    assert_string_arrays_equal(
        testcase.output, a, f"Invalid parser output ({testcase.file}, line {testcase.line})"
    )


def test_parser(testcase: DataDrivenTestCase) -> None:
    """Perform a single native parser test case.

    The argument contains the description of the test case.
    """
    options = Options()
    options.hide_error_codes = True

    if testcase.file.endswith("python310.test"):
        options.python_version = (3, 10)
    elif testcase.file.endswith("python311.test"):
        options.python_version = (3, 11)
    elif testcase.file.endswith("python312.test"):
        options.python_version = (3, 12)
    elif testcase.file.endswith("python313.test"):
        options.python_version = (3, 13)
    elif testcase.file.endswith("python314.test"):
        options.python_version = (3, 14)
    else:
        options.python_version = defaults.PYTHON3_VERSION

    source = "\n".join(testcase.input)

    # Apply mypy: comments to options.
    comments = get_mypy_comments(source)
    changes, _ = parse_mypy_comments(comments, options)
    options = options.apply_changes(changes)

    # Check if we should skip function bodies (when ignoring errors)
    skip_function_bodies = "# mypy: ignore-errors=True" in source

    try:
        with temp_source(source) as fnam:
            node, errors, type_ignores = native_parse(fnam, options, None, skip_function_bodies)
            errors += load_tree(node, options)
            node.path = "main"
            a = node.str_with_options(options).split("\n")
            a = [format_error(err) for err in errors] + a
            a = [format_ignore(ignore) for ignore in type_ignores] + a
    except CompileError as e:
        a = e.messages
    assert_string_arrays_equal(
        testcase.output, a, f"Invalid parser output ({testcase.file}, line {testcase.line})"
    )

