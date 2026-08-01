
def _circulant(c: Array) -> Array:
  n, = c.shape
  idx = (jnp.arange(n)[:, None] - jnp.arange(n)[None, :]) % n
  return c[idx]

