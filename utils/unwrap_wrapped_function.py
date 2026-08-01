
def unwrap_wrapped_function(
    func: Any,
    *,
    unwrap_partial: bool = True,
    unwrap_class_static_method: bool = True,
) -> Any:
    """Recursively unwraps a wrapped function until the underlying function is reached.
    This handles property, functools.partial, functools.partialmethod, staticmethod, and classmethod.

    Args:
        func: The function to unwrap.
        unwrap_partial: If True (default), unwrap partial and partialmethod decorators.
        unwrap_class_static_method: If True (default), also unwrap classmethod and staticmethod
            decorators. If False, only unwrap partial and partialmethod decorators.

    Returns:
        The underlying function of the wrapped function.
    """
    # Define the types we want to check against as a single tuple.
    unwrap_types = (
        (property, cached_property)
        + ((partial, partialmethod) if unwrap_partial else ())
        + ((staticmethod, classmethod) if unwrap_class_static_method else ())
    )

    while isinstance(func, unwrap_types):
        if unwrap_class_static_method and isinstance(func, (classmethod, staticmethod)):
            func = func.__func__
        elif isinstance(func, (partial, partialmethod)):
            func = func.func
        elif isinstance(func, property):
            func = func.fget  # arbitrary choice, convenient for computed fields
        else:
            # Make coverage happy as it can only get here in the last possible case
            assert isinstance(func, cached_property)
            func = func.func  # type: ignore

    return func

