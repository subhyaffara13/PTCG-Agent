
def _is_local_fn(fn):
    # Functions or Methods
    if hasattr(fn, "__code__"):
        return fn.__code__.co_flags & inspect.CO_NESTED
    # Callable Objects
    else:
        if hasattr(fn, "__qualname__"):
            return "<locals>" in fn.__qualname__
        fn_type = type(fn)
        if hasattr(fn_type, "__qualname__"):
            return "<locals>" in fn_type.__qualname__
    return False

