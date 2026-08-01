
def _get_fn_name(fn):
  if isinstance(fn, functools.partial):
    return _get_fn_name(fn.func)
  return getattr(fn, '__name__', 'unnamed_function')

