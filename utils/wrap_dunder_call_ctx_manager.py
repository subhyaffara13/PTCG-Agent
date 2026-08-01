
def wrap_dunder_call_ctx_manager(self: Any, func: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    Apply self as a ctx manager around a call to func
    """

    # NOTE: do not functools.wraps(func) because we don't ever want this frame to be skipped!
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        with self:
            return func(*args, **kwargs)

    return inner

