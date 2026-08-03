import functools
from typing import Callable

def _raise_hard_error_if_graph_break(
    reason: str,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def deco(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        @functools.wraps(fn)
        def graph_break_as_hard_error(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            try:
                return fn(*args, **kwargs)
            except Unsupported as e:
                raise UnsafeScriptObjectError(e.msg) from e

        return graph_break_as_hard_error

    return deco

