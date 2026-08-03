from typing import Callable

def pass_result_wrapper(fn: Callable) -> Callable:
    """
    Wrapper for passes which currently do not return a PassResult.
    This wrapper makes them return a PassResult containing the modified object
    and True for the "modified" flag.

    Args:
        fn (Callable[Module, Any])

    Returns:
        wrapped_fn (Callable[Module, PassResult])
    """
    if fn is None:
        # pyrefly: ignore [bad-return]
        return None

    @wraps(fn)
    def wrapped_fn(gm):
        res = fn(gm)
        if res is None:
            return PassResult(gm, True)
        if isinstance(res, PassResult):
            return res
        elif isinstance(res, nn.Module):
            return PassResult(res, True)

    if not inspect.isfunction(fn):
        wrapped_fn.__name__ = type(fn).__name__

    return wrapped_fn

