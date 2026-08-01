
def with_native_function_and_index(
    func: Callable[[F, BackendIndex], T],
) -> Callable[[F, BackendIndex], T]:
    @functools.wraps(func)
    def wrapper(f: F, backend_index: BackendIndex) -> T:
        with native_function_manager(f):
            return func(f, backend_index)

    return wrapper

