from typing import Callable

def _skipped_function_for_test_reconstruct(
    f: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
) -> _T:
    return f(*args, **kwargs)

