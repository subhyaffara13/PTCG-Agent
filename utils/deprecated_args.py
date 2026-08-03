from typing import Callable, List, Optional

def deprecated_args(
    args_to_warn: Optional[List[str]] = None,
    allowed_args: Optional[List[str]] = None,
    reason: str = "",
    version: str = "",
) -> Callable[[C], C]:
    """
    Decorator to mark specified args of a function as deprecated.
    If '*' is in args_to_warn, all arguments will be marked as deprecated.
    """
    if args_to_warn is None:
        args_to_warn = ["*"]
    if allowed_args is None:
        allowed_args = []

    def _check_deprecated_args(func, filterable_args):
        """Check and warn about deprecated arguments."""
        for arg in args_to_warn:
            if arg == "*" and len(filterable_args) > 0:
                warn_deprecated_arg_usage(
                    list(filterable_args.keys()),
                    func.__name__,
                    reason,
                    version,
                    stacklevel=5,
                )
            elif arg in filterable_args:
                warn_deprecated_arg_usage(
                    arg, func.__name__, reason, version, stacklevel=5
                )

    def decorator(func: C) -> C:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                filterable_args = _get_filterable_args(func, args, kwargs, allowed_args)
                _check_deprecated_args(func, filterable_args)
                return await func(*args, **kwargs)

            return async_wrapper
        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                filterable_args = _get_filterable_args(func, args, kwargs, allowed_args)
                _check_deprecated_args(func, filterable_args)
                return func(*args, **kwargs)

            return wrapper

    return decorator

