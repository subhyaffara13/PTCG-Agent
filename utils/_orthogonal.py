
def _orthogonal(key, n, _m, shape, dtype):
  z = normal(key, (*shape, max(n, _m), min(n, _m)), dtype)
  q, r = jnp_linalg.qr(z)
  d = jnp_linalg.diagonal(r)
  x = q * jnp.expand_dims(jnp.sign(d), -2)

  if n < _m:
    return x.mT
  else:
    return x

