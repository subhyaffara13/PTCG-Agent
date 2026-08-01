
def test_reveal(path: str) -> None:
    """Validate that mypy correctly infers the return-types of
    the expressions in `path`.
    """
    __tracebackhide__ = True

    output_mypy = OUTPUT_MYPY
    if path not in output_mypy:
        return

    relpath = os.path.relpath(path)

    # collect any reported errors, and clean up the output
    failures = []
    for error_line in output_mypy[path]:
        lineno, error_msg = _strip_filename(error_line)
        error_msg = textwrap.indent(error_msg, _FAIL_INDENT)
        reason = _FAIL_MSG_REVEAL.format(relpath, lineno, error_msg)
        failures.append(reason)

    if failures:
        reasons = _FAIL_SEP.join(failures)
        pytest.fail(reasons, pytrace=False)

