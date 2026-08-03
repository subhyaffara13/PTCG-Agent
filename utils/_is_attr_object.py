from typing import Any

def _is_attr_object(obj: Any) -> bool:
    """Check if an object was created with attrs module."""
    return _has_attrs and _attr_module.has(type(obj))


def _is_attr_object(obj: Any) -> bool:
    """Check if an object was created with attrs module."""
    return _has_attrs and _attr_module.has(type(obj))

