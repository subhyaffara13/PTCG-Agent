
def _output_as_string(lines: list[str], line_separator: str) -> str:
    return line_separator.join(_normalize_empty_lines(lines))

