from typing import Any

def _validate_literal(name: str, value: Any, args: tuple[Any, ...]) -> None:
    """Validate Literal type."""
    if isinstance(value, bool):
        if value not in [arg for arg in args if isinstance(arg, bool)]:
            raise TypeError(f"Field '{name}' expected one of {args}, got {value}")
    elif isinstance(value, int):
        if value not in [arg for arg in args if isinstance(arg, int) and not isinstance(arg, bool)]:
            raise TypeError(f"Field '{name}' expected one of {args}, got {value}")
    elif value not in args:
        raise TypeError(f"Field '{name}' expected one of {args}, got {value}")

