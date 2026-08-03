from typing import Callable

def multi_weakref_lru_cache(
    call: Callable,
    *,
    maxsize: int | None = 2048,
    trace_context_in_key: bool = True,
):
  """Least recently used cache decorator with weakref support.

  Similar to `weakref_lru_cache`, except that it keeps weak references
  to all positional and keyword arguments for which
  `is_weakref_cache_key_type()` is true, and strong references to
  other arguments. The cache entry is removed if any of the weakref
  arguments dies.
  """
  cached_call = lib_weakref_lru_cache.multi_weakref_lru_cache(
      config.trace_context if trace_context_in_key else _ignore,
      call,
      maxsize=maxsize,
      explain=None,
      registry=_multi_weakref_registry,
      weak_types=weakref_cache_key_types,
  )
  register_cache(cached_call, str(call))
  return cached_call

