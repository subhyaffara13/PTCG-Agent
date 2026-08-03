from typing import Callable

def triton_builtin(f: Callable[..., _T]) -> Callable[..., _T]:
    """
    Decorator to mark a function as a Triton built-in function.  These functions
    are evaluated at compile time.

    Args:
        f (function): The function to be marked as a Triton built-in.

    Returns:
        function: The same function, marked as a Triton built-in.
    """
    if builtins_use_semantic_kwarg:
        # support Triton before and after https://github.com/triton-lang/triton/pull/7054
        # and after https://github.com/triton-lang/triton/pull/7239
        def wrapper(*args, _semantic, **kwargs):
            kwargs["_builder"] = _semantic
            return f(*args, **kwargs)
    else:
        wrapper = f  # type: ignore[assignment]

    wrapper.__triton_builtin__ = True  # type: ignore[attr-defined]
    return wrapper

