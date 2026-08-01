
def _geometric(key, p, shape, dtype, out_sharding) -> Array:
  check_arraylike("geometric", p)
  p, = promote_dtypes_inexact(p)
  u = uniform(key, shape, p.dtype, out_sharding=out_sharding)
  # TODO(jakevdp): switch to log_u = lax.log1p(u - 1)
  # For now we map u=0 to u=1 to avoid inf in log_u without otherwise
  # changing samples produced for a given key.
  u = jnp.where(u == 0, 1, u)
  log_u = lax.log(u)
  log_one_minus_p = lax.log1p(-p)
  log_one_minus_p = jnp.broadcast_to(log_one_minus_p, shape, out_sharding=out_sharding)
  g = lax.floor(lax.div(log_u, log_one_minus_p)) + 1
  return g.astype(dtype)

