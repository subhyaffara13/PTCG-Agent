
def _is_simplex(x: Array) -> Array:
  x_sum = jnp.sum(x, axis=0)
  return jnp.all(x > 0, axis=0) & (abs(x_sum - 1) < 1E-6)

