
def lru_cache(
    *,
    maxsize: int | None = ...,
    typed: bool = ...,
    always_checkpoint: bool = ...,
    ttl: int | None = ...,
) -> _LRUCacheWrapper: ...


def lru_cache(  # type: ignore[overload-overlap]
    func: Callable[P, Coroutine[Any, Any, T]], /
) -> AsyncLRUCacheWrapper[P, T]: ...


def lru_cache(func: Callable[..., T], /) -> functools._lru_cache_wrapper[T]: ...


def lru_cache(
    func: Callable[..., Coroutine[Any, Any, Any]] | Callable[..., Any] | None = None,
    /,
    *,
    maxsize: int | None = 128,
    typed: bool = False,
    always_checkpoint: bool = False,
    ttl: int | None = None,
) -> Any:
    """
    An asynchronous version of :func:`functools.lru_cache`.

    If a synchronous function is passed, the standard library
    :func:`functools.lru_cache` is applied instead.

    :param always_checkpoint: if ``True``, every call to the cached function will be
        guaranteed to yield control to the event loop at least once
    :param ttl: time in seconds after which to invalidate cache entries

    .. note:: Caches and locks are managed on a per-event loop basis.

    """
    if func is None:
        return _LRUCacheWrapper(maxsize, typed, always_checkpoint, ttl)

    if not callable(func):
        raise TypeError("the first argument must be callable")

    return _LRUCacheWrapper(maxsize, typed, always_checkpoint, ttl)(func)


def lru_cache(
    maxsize: int | None,
) -> Callable[[Callable[..., _T]], functools._lru_cache_wrapper[_T]]:
    def inner(f: Callable[..., _T]) -> functools._lru_cache_wrapper[_T]:
        wrapped_f = functools.lru_cache(maxsize)(f)
        old_cache_clear = wrapped_f.cache_clear
        prev_hits = 0
        prev_misses = 0

        # TODO: There's a ref-cycle here (wrapped_f -> cumulative_cache_info
        # -> wrapped_f) but cannot be solved with weakref as wrapped_f is not
        # weakref'able on some versions of Python

        def cumulative_cache_info() -> functools._CacheInfo:
            cur = wrapped_f.cache_info()
            return functools._CacheInfo(
                prev_hits + cur.hits,
                prev_misses + cur.misses,
                cur.maxsize,
                cur.currsize,
            )

        def new_cache_clear() -> None:
            nonlocal prev_hits, prev_misses
            cur = wrapped_f.cache_info()
            prev_hits += cur.hits
            prev_misses += cur.misses
            old_cache_clear()

        wrapped_f.cache_clear = new_cache_clear  # type: ignore[attr-defined, method-assign]
        wrapped_f.cumulative_cache_info = cumulative_cache_info  # type: ignore[attr-defined, method-assign]
        if log.isEnabledFor(logging.DEBUG):
            atexit.register(log_lru_cache_stats, wrapped_f)  # type: ignore[arg-type]
        return wrapped_f

    return inner


def lru_cache(*, maxsize: int | None = 128) -> Callable[[CallableT], CallableT]:
    """A version of functools.lru_cache that retains the type signature
    for the wrapped function arguments.
    """
    wrapper = functools.lru_cache(  # noqa: TID251
        maxsize=maxsize,
    )
    return cast(Any, wrapper)  # type: ignore[no-any-return]

