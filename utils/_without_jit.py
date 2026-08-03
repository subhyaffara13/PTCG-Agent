import functools

def _without_jit(fn, **unused_kwargs):
  """Variant that does not apply `jax.jit` to a fn (identity)."""

  @functools.wraps(fn)
  def wrapper(*args, **kwargs):
    return fn(*args, **kwargs)

  return wrapper

