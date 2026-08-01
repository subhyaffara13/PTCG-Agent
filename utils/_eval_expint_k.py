
def _eval_expint_k(A: ArrayLike, B: ArrayLike, x: Array) -> Array:
  # helper function for all subsequent intervals
  one = _lax_const(x, 1.0)
  w = one / x
  f = jnp.polyval(A, w) / jnp.polyval(B, w)
  f = w * f + one
  return jnp.exp(x) * w * f

