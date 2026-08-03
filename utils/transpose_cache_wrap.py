import functools
from typing import Any

def transpose_cache_wrap(transpose: Any) -> Any:
    """Decorates a ``transpose()`` implementation to be memoized inside a
    :func:`shared_intermediates` context.
    """

    @functools.wraps(transpose)
    def cached_transpose(a, axes, backend="numpy"):
        if not currently_sharing():
            return transpose(a, axes, backend=backend)

        # hash by axes
        _save_tensors(a)
        axes = tuple(axes)
        key = "transpose", backend, id(a), axes
        return _memoize(key, transpose, a, axes, backend=backend)

    return cached_transpose

