
def weakref_handle(
    ob: object,
    name: str,
    timeout: float,
    loop: asyncio.AbstractEventLoop,
    timeout_ceil_threshold: float = 5,
) -> asyncio.TimerHandle | None:
    if timeout is not None and timeout > 0:
        when = loop.time() + timeout
        if timeout >= timeout_ceil_threshold:
            when = ceil(when)

        return loop.call_at(when, _weakref_handle, (weakref.ref(ob), name))
    return None

