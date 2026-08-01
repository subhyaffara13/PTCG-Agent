
def _erfcx_asymptotic(x: Array, nterms: int) -> Array:
  # Asymptotic expansion: erfcx(x) ~ (1/(sqrt(pi)*x)) * P(1/x^2)
  # P(t) = sum_{k=0}^{N} c_k * t^k,  c_k = (-1)^k * (2k-1)!! / 2^k
  # Coefficients in descending order of degree (k=8..0) for jnp.polyval.
  _coeffs = [7918.06640625, -1055.7421875, 162.421875, -29.53125, 6.5625,
             -1.875, .75, -.5, 1.]
  t = _lax_const(x, 1.) / lax.square(x)
  p = jnp.polyval(np.array(_coeffs[-nterms:], dtype=x.dtype), t)
  return p / (x * _lax_const(x, np.sqrt(np.pi)))

