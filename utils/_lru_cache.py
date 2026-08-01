
def _lru_cache(fn: Callable[P, R]) -> Callable[P, R]:
    """LRU cache decorator with TypeError fallback.

    Provides LRU caching with a fallback mechanism that calls the original
    function if caching fails due to unhashable arguments. Uses a cache
    size of 64 with typed comparison.

    Args:
        fn: The function to be cached.

    Returns:
        A wrapper function that attempts caching with fallback to original function.
    """
    cached_fn = lru_cache(maxsize=64, typed=True)(fn)

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return cached_fn(*args, **kwargs)
        except TypeError:
            return fn(*args, **kwargs)

    return wrapper


def _lru_cache(
    fn: Callable[..., _T], maxsize: int | None = None
) -> functools._lru_cache_wrapper[_T]:
    """
    Wrapper around lru_cache that clears when new info about shapes has been
    updated.

    Use lru_cache if the output is always the same, regardless of the
    constraints we know now (i.e. evaluate_expr)

    Use _lru_cache otherwise.

    Also note that this depends on _update_version_counter being called on the
    shape environment whenever the constraints are updated, otherwise the cache
    will not be cleared.
    """
    fn_cache = lru_cache(maxsize)(fn)
    prior_version = 0

    if config.validate_shape_env_version_key:
        prior_key = None

        @functools.wraps(fn)
        def wrapper(self: ShapeEnv, *args: Any, **kwargs: Any) -> _T:
            nonlocal prior_version, prior_key
            if prior_key is None:
                prior_key = self._get_key()

            if prior_version != self._version_counter:
                fn_cache.cache_clear()
                prior_version = self._version_counter
                prior_key = self._get_key()
            else:
                if prior_key != self._get_key():
                    raise AssertionError(
                        "ShapeEnv cache key changed without version being updated!"
                    )

            return fn_cache(self, *args, **kwargs)

    else:

        @functools.wraps(fn)
        def wrapper(self: ShapeEnv, *args: Any, **kwargs: Any) -> _T:  # type: ignore[misc]
            nonlocal prior_version
            if prior_version != self._version_counter:
                fn_cache.cache_clear()
                prior_version = self._version_counter

            return fn_cache(self, *args, **kwargs)

    wrapper.cache_clear = fn_cache.cache_clear  # type: ignore[attr-defined]
    wrapper.cache_info = fn_cache.cache_info  # type: ignore[attr-defined]
    return wrapper  # type: ignore[return-value]

