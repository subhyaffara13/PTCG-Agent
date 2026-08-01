
def set_cached_generic_type(
    parent: type[BaseModel],
    typevar_values: tuple[Any, ...],
    type_: type[BaseModel],
    origin: type[BaseModel] | None = None,
    args: tuple[Any, ...] | None = None,
) -> None:
    """See the docstring of `get_cached_generic_type_early` for more information about why items are cached with
    two different keys.
    """
    _GENERIC_TYPES_CACHE[_early_cache_key(parent, typevar_values)] = type_
    if len(typevar_values) == 1:
        _GENERIC_TYPES_CACHE[_early_cache_key(parent, typevar_values[0])] = type_
    if origin and args:
        _GENERIC_TYPES_CACHE[_late_cache_key(origin, args, typevar_values)] = type_

