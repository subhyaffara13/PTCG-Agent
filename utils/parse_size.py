
def parse_size(value: str) -> int:
    """Parse a size expressed as a string with digits and unit (like `"10MB"`) to an integer (in bytes)."""
    return _parse_with_unit(value, BYTE_UNITS)

