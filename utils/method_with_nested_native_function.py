
def method_with_nested_native_function(
    func: Callable[[S, F3], T],
) -> Callable[[S, F3], T]:
    @functools.wraps(func)
    def wrapper(slf: S, f: F3) -> T:
        with native_function_manager(f[0]):
            return func(slf, f)

    return wrapper

