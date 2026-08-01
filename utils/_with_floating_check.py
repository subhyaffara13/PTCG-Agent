
def _with_floating_check(fn: Function) -> Function:
  def wrapper(*args, **kwargs):
    dtypes, _ = jax.tree.flatten(
        jax.tree.map(lambda x: x.dtype, (args, kwargs)))
    if not all(jnp.issubdtype(dtype, jnp.floating) for dtype in dtypes):
      raise ValueError(
          'MEAN and RUNNING_MEAN Accumulators require floating-point values.'
      )
    return fn(*args, **kwargs)
  return wrapper

