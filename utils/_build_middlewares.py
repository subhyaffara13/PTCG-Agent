from typing import Callable

def _build_middlewares(
    handler: Handler, apps: tuple["Application", ...]
) -> Callable[[Request], Awaitable[StreamResponse]]:
    """Apply middlewares to handler."""
    for app in apps[::-1]:
        for m, _ in app._middlewares_handlers:  # type: ignore[union-attr]
            handler = update_wrapper(partial(m, handler=handler), handler)
    return handler

