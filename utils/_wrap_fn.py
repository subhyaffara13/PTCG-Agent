
def _wrap_fn(old_fn, new_fn):
  # Recover the original function (to support colab reload)
  old_fn = inspect.unwrap(old_fn)

  @functools.wraps(old_fn)
  def decorated(*args, **kwargs):
    return new_fn(old_fn, *args, **kwargs)

  return decorated

