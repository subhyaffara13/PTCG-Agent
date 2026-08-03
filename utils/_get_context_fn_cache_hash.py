from typing import Any, Callable

def _get_context_fn_cache_hash(context_fn: Callable[..., Any]) -> str | None:
    """
    Extract a cache hash from a context_fn used for selective activation checkpointing (SAC).

    The context_fn determines which ops are saved vs recomputed in the SAC region.
    Since context_fn can be an arbitrary Python function, we cannot reliably pickle
    it for cache key generation (pickle only captures the function name, not the code).

    Users must provide a stable hash by setting a `cache_hash` attribute on the context_fn.
    For functools.partial objects, set the cache_hash on the partial object itself, not on
    the underlying function.

    Returns:
        The cache hash if found
        None: If no hash is provided (caller should bypass caching)
    """
    if hasattr(context_fn, "cache_hash"):
        return context_fn.cache_hash

    return None

