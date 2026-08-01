
def _clone_function(f: Callable[..., Any]) -> Callable[..., Any]:
    """Returns a clone of an existing function."""
    f_new = FunctionType(
        f.__code__,
        f.__globals__,
        name=f.__name__,
        argdefs=f.__defaults__,
        closure=f.__closure__,
    )
    f_new.__kwdefaults__ = f.__kwdefaults__
    return update_wrapper(f_new, f)

