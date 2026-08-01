
def _piecewise_constant(boundaries, values, t):
  index = jnp.sum(boundaries < t)
  return jnp.take(values, index)

