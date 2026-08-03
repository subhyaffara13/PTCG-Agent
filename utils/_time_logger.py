import functools
from typing import Callable

def _time_logger(func: Callable[_P, _T]) -> Callable[_P, _T]:
    @functools.wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        with _WaitCounter(f"pytorch.wait_counter.c10d.{func.__name__}").guard():
            func_return = func(*args, **kwargs)
        return func_return

    return wrapper

