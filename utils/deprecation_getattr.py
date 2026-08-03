import functools

def deprecation_getattr(module, deprecations):
  def _getattr(name):
    if name in deprecations:
      message, fn = deprecations[name]
      if fn is None:  # Is the deprecation accelerated?
        raise AttributeError(message)
      warnings.warn(message, DeprecationWarning, stacklevel=2)
      return fn
    raise AttributeError(f'module {module!r} has no attribute {name!r}')

  return _getattr


def deprecation_getattr(module, deprecations):
  @functools.cache
  def getattr(name):
    if name in deprecations:
      message, fn = deprecations[name]
      if fn is None:  # Is the deprecation accelerated?
        raise AttributeError(message)
      warnings.warn(message, DeprecationWarning, stacklevel=2)
      return fn
    raise AttributeError(f"module {module!r} has no attribute {name!r}")

  return getattr

