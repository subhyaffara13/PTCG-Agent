from typing import Callable, List, Optional

def _get_filterable_args(
    func: Callable, args: tuple, kwargs: dict, allowed_args: Optional[List[str]] = None
) -> dict:
    """
    Extract arguments from function call that should be checked for deprecation/experimental warnings.
    Excludes 'self' and any explicitly allowed args.
    """
    arg_names = func.__code__.co_varnames[: func.__code__.co_argcount]
    filterable_args = dict(zip(arg_names, args))
    filterable_args.update(kwargs)
    filterable_args.pop("self", None)
    if allowed_args:
        for allowed_arg in allowed_args:
            filterable_args.pop(allowed_arg, None)
    return filterable_args

