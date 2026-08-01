
def _normalize_empty_lines(lines: list[str]) -> list[str]:
    while lines and lines[-1].strip() == "":
        lines.pop(-1)

    lines.append("")
    return lines

