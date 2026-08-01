
def _normalize_function_or_error(
    target: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any] | None = None,
    arg_types: tuple[Any] | None = None,
    kwarg_types: dict[str, Any] | None = None,
    normalize_to_only_use_kwargs: bool = False,
) -> ArgsKwargsPair:
    """
    Wrapper around normalize_function that never returns None, but
    loudly errors instead
    """
    res = normalize_function(
        target, args, kwargs, arg_types, kwarg_types, normalize_to_only_use_kwargs
    )
    if res is None:
        raise RuntimeError(
            f"Failed to normalize function {target} with args {args} and kwargs {kwargs}"
        )
    else:
        return res

