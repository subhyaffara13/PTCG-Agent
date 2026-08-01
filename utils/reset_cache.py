
def reset_cache() -> None:
  """Get back to pristine, uninitialized state.

  For more information, see the :ref:`persistent compilation cache guide <persistent-compilation-cache>`.
  """
  global _cache
  global _cache_initialized
  global _cache_checked
  global _cache_used
  logger.info("Resetting cache at %s.",
               _cache._path if _cache is not None else "<empty>")
  _cache = None
  with _cache_initialized_mutex:
    _cache_initialized = False
    _cache_checked = False
    _cache_used = False

