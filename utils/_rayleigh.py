
def _rayleigh(key, scale, shape, dtype) -> Array:
  u = uniform(key, shape, dtype)
  scale = scale.astype(dtype)
  scale = jnp.broadcast_to(scale, shape)
  log_u = lax.log(u)
  n_two = lax._const(scale, -2)
  sqrt_u = lax.sqrt(lax.mul(log_u, n_two))
  ray = lax.mul(scale, sqrt_u)
  return ray

