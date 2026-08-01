
def _ensure_newline_before_comment(output: list[str]) -> list[str]:
    new_output: list[str] = []

    def is_comment(line: str | None) -> bool:
        return line.startswith("#") if line else False

    for line, prev_line in zip(output, [None, *output], strict=False):
        if is_comment(line) and prev_line != "" and not is_comment(prev_line):
            new_output.append("")
        new_output.append(line)
    return new_output

