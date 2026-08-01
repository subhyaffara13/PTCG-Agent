
def wrap_error(
    e: Exception,
    prefix: Optional[_Str] = None,
    suffix: Optional[_Str] = None,
) -> Exception:
  """Wrap the exception in a new exception with the given prefix."""

  # Lazy-evaluate functions
  prefix = prefix() if callable(prefix) else prefix
  suffix = suffix() if callable(suffix) else suffix
  prefix = prefix or ''
  suffix = '\n' + suffix if suffix else ''
  msg = f'{prefix}{e}{suffix}'

  # Dynamically create an exception for:
  # * Compatibility with caller core (e.g. `except OriginalError`)

  class WrappedException(type(e)):
    """Exception proxy with additional message."""

    def __init__(self, msg):
      # We explicitly bypass super() as the `type(e).__init__` constructor
      # might have special kwargs
      Exception.__init__(self, msg)  # pylint: disable=non-parent-init-called

    def __getattr__(self, name: str):
      # Capture `e` through closure. We do not pass e through __init__
      # to bypass `Exception.__new__` magic which add `__str__` artifacts.
      return getattr(e, name)

    # The wrapped exception might have overwritten `__str__` & cie, so
    # use the base exception ones.
    __repr__ = BaseException.__repr__
    __str__ = BaseException.__str__

  WrappedException.__name__ = type(e).__name__
  WrappedException.__qualname__ = type(e).__qualname__
  WrappedException.__module__ = type(e).__module__
  new_exception = WrappedException(msg)
  new_exception.__cause__ = e.__cause__
  new_exception = new_exception.with_traceback(e.__traceback__)
  return new_exception

