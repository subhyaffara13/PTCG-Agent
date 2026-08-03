from typing import Any

def _wrap_bound_method(fn: Any, argnames: list[str]) -> Any:
    """
    Wrap a bound method to remove 'self' from its signature for FX tracing.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    params = [
        inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        for name in argnames
    ]
    wrapper.__signature__ = inspect.Signature(params)  # type: ignore[attr-defined]
    return wrapper

