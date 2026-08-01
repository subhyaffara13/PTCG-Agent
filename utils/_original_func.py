
def _original_func(f: Callable) -> Callable:
  if isinstance(f, property):
    fget = cast(property, f).fget
    assert fget is not None
    return fget
  elif isinstance(f, functools.cached_property):
    return f.func
  return f

