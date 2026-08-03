from typing import Any, Callable

def call_for_coroutine(
    func: Callable[[Unpack[PosArgsT]], Coroutine[Any, Any, T_co]],
    args: tuple[Unpack[PosArgsT]],
    **kwargs: Any,
) -> Coroutine[Any, Any, T_co]:
    """
    Call the given function with the given positional and keyword arguments.

    :return: the resulting coroutine
    :raises TypeError: if the return value was not a coroutine object

    """
    coro = func(*args, **kwargs)
    if not isinstance(coro, Coroutine):
        prefix = f"{func.__module__}." if hasattr(func, "__module__") else ""
        raise TypeError(
            f"Expected {prefix}{func.__qualname__}() to return a coroutine, but "
            f"the return value ({coro!r}) is not a coroutine object"
        )

    return coro

