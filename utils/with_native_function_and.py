import functools
from typing import Callable

def with_native_function_and(func: Callable[[F, F2], T]) -> Callable[[F, F2], T]:
    @functools.wraps(func)
    def wrapper(f: F, f2: F2) -> T:
        # The first native_function is assumed to be the one with the appropriate context.
        with native_function_manager(f):
            return func(f, f2)

    return wrapper

