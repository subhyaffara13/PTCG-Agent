
def piecewise_constant(boundaries: Any, values: Any):
  boundaries = jnp.array(boundaries)
  values = jnp.array(values)
  if not boundaries.ndim == values.ndim == 1:
    raise ValueError("boundaries and values must be sequences")
  if not boundaries.shape[0] == values.shape[0] - 1:
    raise ValueError("boundaries length must be one shorter than values length")

  def schedule(i):
    return values[jnp.sum(i > boundaries)]
  return schedule

