
def _ball(key, p, d, shape, dtype):
  k1, k2 = split(key)
  g = generalized_normal(k1, p, (*shape, d), dtype)
  e = exponential(k2, shape, dtype)
  return g / (((jnp.abs(g) ** p).sum(-1) + e) ** (1 / p))[..., None]

