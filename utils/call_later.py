from typing import Any, Callable

def call_later(
    cb: Callable[[], Any],
    timeout: float,
    loop: asyncio.AbstractEventLoop,
    timeout_ceil_threshold: float = 5,
) -> asyncio.TimerHandle | None:
    if timeout is None or timeout <= 0:
        return None
    now = loop.time()
    when = calculate_timeout_when(now, timeout, timeout_ceil_threshold)
    return loop.call_at(when, cb)

