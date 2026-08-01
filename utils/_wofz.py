
def _wofz(z: Array) -> Array:
  sign = lax.ge(lax.imag(z), _lax_const(lax.real(z), 0.))
  z_upper = lax.select(sign, z, lax.neg(z))
  w_upper = _wofz_upper(z_upper)
  correction = 2 * lax.exp(lax.neg(z * z)) - w_upper
  return lax.select(sign, w_upper, correction)

