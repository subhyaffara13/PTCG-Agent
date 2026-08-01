
def _resolve_typed_dict_type(typ):
    """Resolve the actual TypedDict class from a potentially wrapped type."""
    from typing_extensions import _TypedDictMeta  # type: ignore

    origin = get_origin(typ)
    if origin is Union:  # Check if it's a Union (like Optional)
        for arg in get_args(typ):
            if isinstance(arg, _TypedDictMeta):
                return arg
    elif isinstance(typ, type) and isinstance(typ, dict):
        return typ
    return None

