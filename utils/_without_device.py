import functools

def _without_device(fn, **unused_kwargs):
  """Variant that applies `jax.device_get` to the args of fn."""

  @functools.wraps(fn)
  def wrapper(*args, **kwargs):

    def get(x):
      if isinstance(x, jax.Array):
        return jax.device_get(x)
      return x

    no_device_args = tree_map(get, args)
    no_device_kwargs = tree_map(get, kwargs)
    return fn(*no_device_args, **no_device_kwargs)

  return wrapper

