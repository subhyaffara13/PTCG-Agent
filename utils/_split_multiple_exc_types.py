
def _split_multiple_exc_types(target: str) -> list[str]:
    delimiters = r"(\s*,(?:\s*or\s)?\s*|\s+or\s+)"
    return re.split(delimiters, target)

