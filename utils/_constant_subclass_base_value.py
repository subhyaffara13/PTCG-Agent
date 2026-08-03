from typing import Any

def _constant_subclass_base_value(value: Any) -> Any:
    """Extract the base constant value from a constant subclass instance."""
    from .variables.user_defined import _CONSTANT_BASE_TYPES

    for t in _CONSTANT_BASE_TYPES:
        if isinstance(value, t):
            return t(value)  # pyrefly: ignore[bad-argument-type]
    raise TypeError(f"Not a constant subclass: {type(value)}")

