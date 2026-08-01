
def experimental_args(
    args_to_warn: Optional[List[str]] = None,
) -> Callable[[C], C]:
    """
    Decorator to mark specified args of a function as experimental.
    If '*' is in args_to_warn, all arguments will be marked as experimental.
    """
    if args_to_warn is None:
        args_to_warn = ["*"]

    def _check_experimental_args(func, filterable_args):
        """Check and warn about experimental arguments."""
        for arg in args_to_warn:
            if arg == "*" and len(filterable_args) > 0:
                warn_experimental_arg_usage(
                    list(filterable_args.keys()), func.__name__, stacklevel=4
                )
            elif arg in filterable_args:
                warn_experimental_arg_usage(arg, func.__name__, stacklevel=4)

    def decorator(func: C) -> C:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                filterable_args = _get_filterable_args(func, args, kwargs)
                if len(filterable_args) > 0:
                    _check_experimental_args(func, filterable_args)
                return await func(*args, **kwargs)

            return async_wrapper
        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                filterable_args = _get_filterable_args(func, args, kwargs)
                if len(filterable_args) > 0:
                    _check_experimental_args(func, filterable_args)
                return func(*args, **kwargs)

            return wrapper

    return decorator

