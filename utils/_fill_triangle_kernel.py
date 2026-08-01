
def _fill_triangle_kernel(x):
  return jnp.maximum(0, 1 - jnp.abs(x))

