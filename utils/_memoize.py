from typing import Any

def _memoize(key: CacheKeyType, fn: Any, *args: Any, **kwargs: Any) -> ArrayType:
    """Memoize ``fn(*args, **kwargs)`` using the given ``key``.
    Results will be stored in the innermost ``cache`` yielded by
    :func:`shared_intermediates`.
    """
    cache = get_sharing_cache()
    if key in cache:
        return cache[key]
    result = fn(*args, **kwargs)
    cache[key] = result
    return result


def _memoize(func):
    memo = {}

    def wrapper(*a, **kw):
        key = repr((a, kw))
        if key not in memo:
            try:
                memo[key] = func(*a, **kw)
            except Exception as e:
                memo[key] = e
                raise
        ret = memo[key]
        if isinstance(ret, Exception):
            raise ret
        return ret

    wrapper.__name__ = func.__name__
    return wrapper


def _memoize(fn):
  cells = {}
  sentinel = object()
  def memoized(*args):
    out = cells.get(args, sentinel)
    if out is sentinel:
      with core.set_current_trace(None):
        out = cells[args] = fn(*args)
    return out
  return memoized


def _memoize(f):
    class memodict(dict):
        def __missing__(self, key):
            ret = f(key)
            if isinstance(key, int) or len(key) == 1:
                self[key] = ret
            return ret

    return memodict().__getitem__

