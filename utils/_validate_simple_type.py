from typing import Any

def _validate_simple_type(name: str, value: Any, expected_type: type) -> None:
    """Validate simple type (int, str, etc.)."""
    if expected_type is int and isinstance(value, bool):
        raise TypeError(
            f"Field '{name}' expected {expected_type.__name__}, got {type(value).__name__} (value: {repr(value)})"
        )
    if not isinstance(value, expected_type):
        raise TypeError(
            f"Field '{name}' expected {expected_type.__name__}, got {type(value).__name__} (value: {repr(value)})"
        )

