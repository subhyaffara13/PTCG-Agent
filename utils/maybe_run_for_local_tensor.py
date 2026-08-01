
def maybe_run_for_local_tensor(func: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    Decorator that ensures a function is executed for each local tensor shard
    when running under LocalTensorMode. If not in LocalTensorMode, the function
    is executed normally. When in LocalTensorMode, the function is run for each
    rank, and the results are collected appropriately.

    This decorator is useful for functions that exhibit non-SPMD behavior, such
    as those requiring rank specific actions. For example, a function that computes
    offset into input tensor based on rank.

    Note that the function being decorated must not have any side effects and
    contain operations for a single rank only. For example, wrapping a function
    that performs a collective operation will not work.

    Args:
        func (Callable[..., Any]): The function to be decorated.

    Returns:
        Callable[..., Any]: The wrapped function that handles LocalTensorMode logic.
    """

    @functools.wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        if not (lm := enabled_local_tensor_mode()):
            return func(*args, **kwargs)
        ret = None
        with lm.disable():
            ret = _for_each_rank_run_func(func, lm.ranks, args, kwargs, alias=False)

        return ret

    return wrapper

