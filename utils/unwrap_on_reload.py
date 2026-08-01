
def unwrap_on_reload(fn: _FnT) -> _FnT:
  """Unwrap the function to support colab module reload."""
  return getattr(fn, '__original_fn__', fn)

