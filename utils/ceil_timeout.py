
def ceil_timeout(
    delay: float | None, ceil_threshold: float = 5
) -> async_timeout.Timeout:
    if delay is None or delay <= 0:
        return async_timeout.timeout(None)

    loop = asyncio.get_running_loop()
    now = loop.time()
    when = now + delay
    if delay > ceil_threshold:
        when = ceil(when)
    return async_timeout.timeout_at(when)

