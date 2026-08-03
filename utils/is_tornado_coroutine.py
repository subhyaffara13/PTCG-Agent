import sys

def is_tornado_coroutine(func):
    """Return whether `func` is a Tornado coroutine function.

    Running coroutines are not supported.
    """
    warnings.warn(
        "is_tornado_coroutine is deprecated in cloudpickle 3.0 and will be "
        "removed in cloudpickle 4.0. Use tornado.gen.is_coroutine_function "
        "directly instead.",
        category=DeprecationWarning,
    )
    if "tornado.gen" not in sys.modules:
        return False
    gen = sys.modules["tornado.gen"]
    if not hasattr(gen, "is_coroutine_function"):
        # Tornado version is too old
        return False
    return gen.is_coroutine_function(func)

