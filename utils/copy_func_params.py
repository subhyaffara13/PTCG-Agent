
def copy_func_params(
    source_func: Callable[_P, Any],
) -> Callable[[Callable[..., _R]], Callable[_P, _R]]:
    """Cast the decorated function's call signature to the source_func's.

    Usage:
        def upstream_func(a: int, b: float, *, double: bool = False) -> float: ...
        @copy_func_params(upstream_func)
        def enhanced(a: int, b: float, *args: Any, double: bool = False, **kwargs: Any) -> str: ...
    """

    def return_func(func: Callable[..., _R]) -> Callable[_P, _R]:
        return cast(Callable[_P, _R], func)

    return return_func

