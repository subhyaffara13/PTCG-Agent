
def format_ignore(ignore: tuple[int, list[str]]) -> str:
    line, codes = ignore
    if not codes:
        return f"ignore: {line}"
    else:
        return f"ignore: {line} [{', '.join(codes)}]"

