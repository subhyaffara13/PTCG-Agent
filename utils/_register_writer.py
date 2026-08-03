from typing import Any, Callable

def _register_writer(idx: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        _write_dispatch[idx] = func  # noqa: F821
        return func

    return decorator

