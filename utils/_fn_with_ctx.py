from typing import Any, Callable

def _fn_with_ctx(ctx: Any, fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    with ctx:
        return fn(*args, **kwargs)

