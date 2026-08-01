
def _memoize_method(key_fn=lambda x: x):
  """Memoize a single-arg instance method using an on-object cache."""

  def memoizer(method):
    cache_name = "cache_" + method.__name__

    def wrap(self, arg):
      key = key_fn(arg)
      cache = vars(self).setdefault(cache_name, {})
      if key not in cache:
        cache[key] = method(self, arg)
      return cache[key]

    return wrap

  return memoizer

