from typing import Any

def _get_default(value: Any) -> Any:
    """Get default argument value, given the trait default value."""
    return Parameter.empty if value == Undefined else value

