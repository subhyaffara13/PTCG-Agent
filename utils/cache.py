import functools
import time
from typing import Any, Callable

def cache(  # type: ignore[overload-overlap]
    func: Callable[P, Coroutine[Any, Any, T]], /
) -> AsyncLRUCacheWrapper[P, T]: ...


def cache(func: Callable[..., T], /) -> functools._lru_cache_wrapper[T]: ...


def cache(func: Callable[..., Any] | Callable[P, Coroutine[Any, Any, Any]], /) -> Any:
    """
    A convenient shortcut for :func:`lru_cache` with ``maxsize=None``.

    This is the asynchronous equivalent to :func:`functools.cache`.

    """
    return lru_cache(maxsize=None)(func)


def cache(request):
    """
    Fixture for 'cache' argument in to_datetime.
    """
    return request.param


def cache(request: FixtureRequest) -> Cache:
    """Return a cache object that can persist state between testing sessions.

    cache.get(key, default)
    cache.set(key, value)

    Keys must be ``/`` separated strings, where the first part is usually the
    name of your plugin or application to avoid clashes with other cache users.

    Values can be any object handled by the json stdlib module.
    """
    assert request.config.cache is not None
    return request.config.cache


def cache(call: Callable, *,
          explain: Callable[[WrappedFun, bool, dict, tuple, float], None] | None = None):
  """Memoization decorator for functions taking a WrappedFun as first argument.

  Args:
    call: a Python callable that takes a WrappedFun as its first argument. The
      underlying transforms and params on the WrappedFun are used as part of the
      memoization cache key.

    explain: a function that is invoked upon cache misses to log an explanation
      of the miss.
      Invoked with `(fun, is_cache_first_use, cache, key, elapsed_sec)`.

  Returns:
     A memoized version of ``call``.
  """
  fun_caches: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()

  def memoized_fun(fun: WrappedFun, *args):
    cache = fun_caches.setdefault(fun.f, new_cache := {})
    key = (fun.transforms, fun.params, fun.in_type, args, config.trace_context())
    result = cache.get(key, None)
    if result is not None:
      ans, stores = result
      fun.populate_stores(stores)
    else:
      start = 0.0
      if do_explain := explain and config.explain_cache_misses.value:
        start = time.time()
      ans = call(fun, *args)
      if do_explain:
        assert explain
        explain(fun, cache is new_cache, cache, key, time.time() - start)
      cache[key] = (ans, fun.stores)

    return ans

  def _evict_function(f):
    fun_caches.pop(f, None)

  memoized_fun.evict_function = _evict_function  # pyrefly: ignore[missing-attribute]
  memoized_fun.cache_clear = fun_caches.clear  # pyrefly: ignore[missing-attribute]
  register_cache(memoized_fun, str(call))
  return memoized_fun


def cache(max_size=4096, trace_context_in_key: bool | Callable = True):
  if trace_context_in_key:
    trace_context = (trace_context_in_key if callable(trace_context_in_key)
                     else config.trace_context)
    def wrap(f):
      @functools.lru_cache(max_size)
      def cached(_, *args, **kwargs):
        return f(*args, **kwargs)

      @functools.wraps(f)
      def wrapper(*args, **kwargs):
        if config.check_tracer_leaks.value:
          return f(*args, **kwargs)
        return cached(trace_context(), *args, **kwargs)

      wrapper = cast(Any, wrapper)  # avoids missing-attribute typing errors
      wrapper.cache_clear = cached.cache_clear
      wrapper.cache_info = cached.cache_info
      register_cache(wrapper, str(f))
      return wrapper
  else:
    def wrap(f):
      wrapper = functools.lru_cache(max_size)(f)
      register_cache(wrapper, str(f))
      return wrapper
  return wrap

