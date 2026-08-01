
def _hanging_indent_end_line(line: str) -> str:
    if not line.endswith(" "):
        line += " "
    return line + "\\"

