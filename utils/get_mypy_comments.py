
def get_mypy_comments(source: str) -> list[tuple[int, str]]:
    PREFIX = "# mypy: "
    # Don't bother splitting up the lines unless we know it is useful
    if PREFIX not in source:
        return []
    lines = source.split("\n")
    results = []
    for i, line in enumerate(lines):
        if line.startswith(PREFIX):
            results.append((i + 1, line[len(PREFIX) :]))

    return results

