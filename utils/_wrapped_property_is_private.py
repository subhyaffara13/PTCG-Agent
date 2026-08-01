
def _wrapped_property_is_private(property_: cached_property | property) -> bool:  # type: ignore
    """Returns true if provided property is private, False otherwise."""
    wrapped_name: str = ''

    if isinstance(property_, property):
        wrapped_name = getattr(property_.fget, '__name__', '')
    elif isinstance(property_, cached_property):  # type: ignore
        wrapped_name = getattr(property_.func, '__name__', '')  # type: ignore

    return wrapped_name.startswith('_') and not wrapped_name.startswith('__')

