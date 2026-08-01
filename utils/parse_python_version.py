
def parse_python_version(ver_str: str) -> tuple[int, ...]:
    """Convert python version to a tuple of integers for easy comparison."""
    return tuple(int(digit) for digit in ver_str.split("."))

