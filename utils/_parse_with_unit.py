
def _parse_with_unit(value: str, units: dict[str, int]) -> int:
    """Parse a numeric value with optional unit."""
    stripped = value.strip()
    if not stripped:
        raise ValueError("Value cannot be empty.")
    try:
        return int(value)
    except ValueError:
        pass

    match = RE_NUMBER_WITH_UNIT.fullmatch(stripped)
    if not match:
        raise ValueError(f"Invalid value '{value}'. Must match pattern '\\d+[a-z]+' or be a plain number.")

    number = int(match.group(1))
    unit = match.group(2).lower()

    if unit not in units:
        raise ValueError(f"Unknown unit '{unit}'. Must be one of {list(units.keys())}.")

    return number * units[unit]

