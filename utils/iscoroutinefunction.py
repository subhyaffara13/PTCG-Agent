
def iscoroutinefunction(func: object) -> bool:
    """Return True if func is a coroutine function (a function defined with async
    def syntax, and doesn't contain yield), or a function decorated with
    @asyncio.coroutine.

    Note: copied and modified from Python 3.5's builtin coroutines.py to avoid
    importing asyncio directly, which in turns also initializes the "logging"
    module as a side-effect (see issue #8).
    """
    return inspect.iscoroutinefunction(func) or getattr(func, "_is_coroutine", False)

