
def _natural_keys(text: str) -> list[Any]:
    return [_atoi(c) for c in re.split(r"(\d+)", text)]

