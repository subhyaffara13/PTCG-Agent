
def is_lru_cache_wrapped_function(
    value: Callable[..., T],
) -> TypeGuard[functools._lru_cache_wrapper[T]]: ...


def is_lru_cache_wrapped_function(
    value: Any,
) -> TypeGuard[functools._lru_cache_wrapper[Any]]: ...


def is_lru_cache_wrapped_function(
    value: Any,
) -> bool:
    return isinstance(value, functools._lru_cache_wrapper) and is_function(
        inspect.getattr_static(value, "__wrapped__")
    )

