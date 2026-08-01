
def exposed_in(module: str) -> Callable[[F], F]:
    def wrapper(fn: F) -> F:
        fn.__module__ = module
        return fn

    return wrapper

