
def wraps_with_reload(fn: Callable[..., Any]) -> Callable[[_FnT], _FnT]:
  """Wrap the function to support colab module reload."""

  def decorator(fn_to_wrap):
    fn_to_wrap = functools.wraps(fn)(fn_to_wrap)
    fn_to_wrap.__original_fn__ = fn
    return fn_to_wrap

  return decorator

