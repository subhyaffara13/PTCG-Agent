
def deprecated_function(reason="", version="", name=None):
    """
    Decorator to mark a function as deprecated.
    """

    def decorator(func):
        if inspect.iscoroutinefunction(func):
            # Create async wrapper for async functions
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                warn_deprecated(name or func.__name__, reason, version, stacklevel=3)
                return await func(*args, **kwargs)

            return async_wrapper
        else:
            # Create regular wrapper for sync functions
            @wraps(func)
            def wrapper(*args, **kwargs):
                warn_deprecated(name or func.__name__, reason, version, stacklevel=3)
                return func(*args, **kwargs)

            return wrapper

    return decorator

