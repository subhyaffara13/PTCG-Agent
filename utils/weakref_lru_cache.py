
def weakref_lru_cache(
    f: Callable[P, R], /, *, maxsize: int | None = 2048,
    trace_context_in_key: bool = True, explain: Callable | None = None
) -> WeakrefCachedFunc[P, R]: ...


def weakref_lru_cache(
    f: None = None, /, *, maxsize: int | None = 2048,
    trace_context_in_key: bool = True, explain: Callable | None = None
) -> Callable[[Callable[P, R]], WeakrefCachedFunc[P, R]]: ...


def weakref_lru_cache(
    f: Callable[P, R] | None = None, *, maxsize: int | None = 2048,
    trace_context_in_key: bool = True, explain: Callable | None = None
):
  """
  Least recently used cache decorator with weakref support.

  The cache will take a weakref to the first argument of the wrapped function
  and strong refs to all other arguments. In all other respects it should
  behave similar to `functools.lru_cache`. The cache is thread local.
  """
  kwargs = dict(maxsize=maxsize, trace_context_in_key=trace_context_in_key,
                explain=explain)
  if f is None:
    return lambda g: _weakref_lru_cache(g, **kwargs)
  return _weakref_lru_cache(f, **kwargs)

