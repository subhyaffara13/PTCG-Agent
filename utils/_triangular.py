
def _triangular(key, left, mode, right, shape, dtype) -> Array:
  # https://en.wikipedia.org/wiki/Triangular_distribution#Generating_triangular-distributed_random_variates
  left = jnp.broadcast_to(lax.convert_element_type(left, dtype), shape)
  right = jnp.broadcast_to(lax.convert_element_type(right, dtype), shape)
  mode = jnp.broadcast_to(lax.convert_element_type(mode, dtype), shape)
  fc = (mode - left) / (right - left)
  u = uniform(key, shape, dtype)
  out1 = left + lax.sqrt(u * (right - left) * (mode - left))
  out2 = right - lax.sqrt((1 - u) * (right - left) * (right - mode))
  tri = lax.select(u < fc, out1, out2)
  return tri

