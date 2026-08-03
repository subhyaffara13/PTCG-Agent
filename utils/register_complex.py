from typing import Any, Callable

def register_complex(
    op: OpType,
    func_impl: Callable[..., Any] | None = None,
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]] | Callable[..., Any]:
    """Decorator to register an implementation for some ops in some dispatch tables"""

    def inner(func: Callable[_P, _R]) -> Callable[_P, _R]:
        if COMPLEX_OPS_TABLE.get(op, func) is not func:
            raise RuntimeError(f"Attempted to register multiple functions for {op}")
        COMPLEX_OPS_TABLE[op] = func
        return func

    if func_impl is None:
        return inner

    return inner(func_impl)

