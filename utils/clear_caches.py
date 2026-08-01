
def clear_caches() -> None:
    """Jinja keeps internal caches for environments and lexers.  These are
    used so that Jinja doesn't have to recreate environments and lexers all
    the time.  Normally you don't have to care about that but if you are
    measuring memory consumption you may want to clean the caches.
    """
    from .environment import get_spontaneous_environment
    from .lexer import _lexer_cache

    get_spontaneous_environment.cache_clear()
    _lexer_cache.clear()


def clear_caches() -> None:
    """
    Clear all registered caches.
    """
    for obj in _registered_caches:
        obj.cache_clear()


def clear_caches():
  """Clear all compilation and staging caches.

  This doesn't clear the persistent cache; to disable it (e.g. for benchmarks),
  set the jax_enable_compilation_cache config option to False.
  """
  # Clear all lu.cache, util.cache and util.weakref_lru_cache instances
  # (used for staging and Python-dispatch compiled executable caches).
  util.clear_all_caches()
  # Clear all C++ compiled executable caches for pjit
  pjit._cpp_pjit_cache_fun_only.clear()
  pjit._cpp_pjit_cache_explicit_attributes.clear()
  _jax.PjitFunctionCache.clear_all()

