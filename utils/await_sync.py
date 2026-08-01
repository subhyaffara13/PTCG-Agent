
def await_sync(awaitable: Awaitable[T]) -> T:
    with get_loop() as loop:
        return loop.run_until_complete(awaitable)

