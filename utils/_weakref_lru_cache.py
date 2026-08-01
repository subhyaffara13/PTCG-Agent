
def _weakref_lru_cache(f, maxsize, trace_context_in_key, explain):
  cached_f = lib_weakref_lru_cache.weakref_lru_cache(
      config.trace_context if trace_context_in_key else _ignore, f, maxsize,
      explain = lambda: explain if config.explain_cache_misses.value else None)
  register_cache(cached_f, str(f))
  return cached_f

