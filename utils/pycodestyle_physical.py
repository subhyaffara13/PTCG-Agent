
def pycodestyle_physical(
    indent_char: Any,
    line_number: Any,
    lines: Any,
    max_line_length: Any,
    multiline: Any,
    noqa: Any,
    physical_line: Any,
    total_lines: Any,
) -> Generator[tuple[int, str]]:
    """Run pycodestyle physical checks."""
    ret = _maximum_line_length(physical_line, max_line_length, multiline, line_number, noqa)  # noqa: E501
    if ret is not None:
        yield ret
    ret = _tabs_obsolete(physical_line)
    if ret is not None:
        yield ret
    ret = _tabs_or_spaces(physical_line, indent_char)
    if ret is not None:
        yield ret
    ret = _trailing_blank_lines(physical_line, lines, line_number, total_lines)
    if ret is not None:
        yield ret
    ret = _trailing_whitespace(physical_line)
    if ret is not None:
        yield ret

