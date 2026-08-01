
def wraps_cls(wrapped: type[Any]) -> Callable[[_Cls], _Cls]:
  """Equivalent of `functools.wraps` but for classes."""

  def decorator(cls):
    cls.__name__ = wrapped.__name__
    cls.__qualname__ = wrapped.__qualname__
    cls.__doc__ = wrapped.__doc__
    cls.__module__ = wrapped.__module__
    return cls

  return decorator

