from typing import Any

def get_cached_generic_type_late(
    parent: type[BaseModel], typevar_values: Any, origin: type[BaseModel], args: tuple[Any, ...]
) -> type[BaseModel] | None:
    """See the docstring of `get_cached_generic_type_early` for more information about the two-stage cache lookup."""
    cached = _GENERIC_TYPES_CACHE.get(_late_cache_key(origin, args, typevar_values))
    if cached is not None:
        set_cached_generic_type(parent, typevar_values, cached, origin, args)
    return cached

