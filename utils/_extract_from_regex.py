
def _extract_from_regex(duration: str) -> Tuple[int, str]:
    match = re.match(r"(\d+)(mo|[smhdw]?)", duration)

    if not match:
        raise ValueError("Invalid duration format")

    value, unit = match.groups()
    value = int(value)

    return value, unit

