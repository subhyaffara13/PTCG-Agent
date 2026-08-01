
def register_cache(cls: type[BaseCache], clobber: bool = False) -> None:
    """'Register' cache implementation.

    Parameters
    ----------
    clobber: bool, optional
        If set to True (default is False) - allow to overwrite existing
        entry.

    Raises
    ------
    ValueError
    """
    name = cls.name
    if not clobber and name in caches:
        raise ValueError(f"Cache with name {name!r} is already known: {caches[name]}")
    caches[name] = cls


def register_cache(cache: Any, for_what: str):
  """Registers a cache with JAX's cache management.

  Args:
    cache: an object supporting `cache_clear()`, `cache_info()`, and
      `cache_keys()`, like the result of `functools.lru_cache()`.
    for_what: a string to identify what this cache is used for. This is
       used for debugging.
  """
  _caches[cache] = for_what

