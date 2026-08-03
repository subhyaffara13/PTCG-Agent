from typing import Any

def _get_int(value: Any, default: int) -> int:
    """Cast config value to int with default."""
    if value is None:
        return default
    return int(value)


def _get_int(value: Any, default: int) -> int:
    """Cast config value to int with default."""
    if value is None:
        return default
    return int(value)

