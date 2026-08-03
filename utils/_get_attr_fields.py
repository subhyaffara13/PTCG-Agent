from typing import Any

def _get_attr_fields(obj: Any) -> Sequence["_attr_module.Attribute[Any]"]:
    """Get fields for an attrs object."""
    return _attr_module.fields(type(obj)) if _has_attrs else []


def _get_attr_fields(obj: Any) -> Sequence["_attr_module.Attribute[Any]"]:
    """Get fields for an attrs object."""
    return _attr_module.fields(type(obj)) if _has_attrs else []

