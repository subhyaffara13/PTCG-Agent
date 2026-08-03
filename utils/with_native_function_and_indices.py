import functools
from typing import Callable

def with_native_function_and_indices(
    func: Callable[[F, dict[DispatchKey, BackendIndex]], T],
) -> Callable[[F, dict[DispatchKey, BackendIndex]], T]:
    @functools.wraps(func)
    def wrapper(f: F, backend_indices: dict[DispatchKey, BackendIndex]) -> T:
        with native_function_manager(f):
            return func(f, backend_indices)

    return wrapper

