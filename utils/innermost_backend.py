from typing import Any, Callable

def innermost_backend(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Unwrap backend wrapper chain via _torchdynamo_orig_backend to find the
    innermost backend function.
    """
    while hasattr(fn, "_torchdynamo_orig_backend"):
        fn = fn._torchdynamo_orig_backend
        assert callable(fn), (
            f"A callable function is expected, but {type(fn)} is provided."
        )
    return fn

