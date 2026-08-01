
def ensure_returns_coro(
    func: Callable[P, Awaitable[T_Retval]],
) -> Callable[P, Coroutine[Any, Any, T_Retval]]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Coroutine[Any, Any, T_Retval]:
        awaitable = func(*args, **kwargs)
        # Check the common case first.
        if isinstance(awaitable, Coroutine):
            return awaitable
        elif not isinstance(awaitable, Awaitable):
            # The user violated the type annotations. Still, we should pass this on to
            # Trio so it can raise with an appropriate message.
            return awaitable
        else:

            @wraps(func)
            async def inner_wrapper() -> T_Retval:
                return await awaitable

            return inner_wrapper()

    return wrapper

