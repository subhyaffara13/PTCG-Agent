import functools
from typing import Callable

def wrap_inline(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    Create an extra frame around fn that is not in skipfiles.
    """

    @functools.wraps(fn)
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        return fn(*args, **kwargs)

    return inner

