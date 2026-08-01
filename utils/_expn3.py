
def _expn3(x: Array, n: Array) -> Array:
  # n >= 5000
  _c = _lax_const
  one = _c(x, 1.0)
  xk = x + n
  yk = one / (xk * xk)
  t = n
  ans = yk * t * (_c(x, 6) * x * x - _c(x, 8) * t * x + t * t)
  ans = yk * (ans + t * (t - _c(x, 2) * x))
  ans = yk * (ans + t)
  return (ans + one) * jnp.exp(-x) / xk

