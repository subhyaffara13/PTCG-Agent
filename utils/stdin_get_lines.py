
def stdin_get_lines() -> list[str]:
    """Return lines of stdin split according to file splitting."""
    return list(io.StringIO(stdin_get_value()))

