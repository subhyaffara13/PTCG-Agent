
def is_async_function(func: object) -> bool:
    """Return True if the given function seems to be an async function or
    an async generator."""
    return iscoroutinefunction(func) or inspect.isasyncgenfunction(func)

