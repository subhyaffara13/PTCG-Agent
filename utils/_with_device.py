
def _with_device(fn, ignore_argnums=(), static_argnums=(), **unused_kwargs):
  """Variant that applies `jax.device_put` to the args of fn."""

  if isinstance(ignore_argnums, int):
    ignore_argnums = (ignore_argnums,)
  if isinstance(static_argnums, int):
    static_argnums = (static_argnums,)

  @functools.wraps(fn)
  def wrapper(*args, **kwargs):

    def put(x):
      try:
        return jax.device_put(x)
      except TypeError:  # not a valid JAX type
        return x

    device_args = [
        arg if (idx in ignore_argnums or idx in static_argnums) else tree_map(
            put, arg) for idx, arg in enumerate(args)
    ]
    device_kwargs = tree_map(put, kwargs)
    return fn(*device_args, **device_kwargs)

  return wrapper

