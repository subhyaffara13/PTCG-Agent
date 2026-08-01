
def experimental_method() -> Callable[[C], C]:
    """
    Decorator to mark a function as experimental.
    """

    def decorator(func: C) -> C:
        if inspect.iscoroutinefunction(func):
            # Create async wrapper for async functions
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                warn_experimental(func.__name__, stacklevel=2)
                return await func(*args, **kwargs)

            return async_wrapper
        else:
            # Create regular wrapper for sync functions
            @wraps(func)
            def wrapper(*args, **kwargs):
                warn_experimental(func.__name__, stacklevel=2)
                return func(*args, **kwargs)

            return wrapper

    return decorator

