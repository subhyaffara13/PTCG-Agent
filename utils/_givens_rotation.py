
def _givens_rotation(a, b):
  b_zero = abs(b) == 0
  a_lt_b = abs(a) < abs(b)
  t = -jnp.where(a_lt_b, a, b) / jnp.where(a_lt_b, b, a)
  r = lax.rsqrt(1 + abs(t) ** 2).astype(t.dtype)
  cs = jnp.where(b_zero, 1, jnp.where(a_lt_b, r * t, r))
  sn = jnp.where(b_zero, 0, jnp.where(a_lt_b, r, r * t))
  return cs, sn

