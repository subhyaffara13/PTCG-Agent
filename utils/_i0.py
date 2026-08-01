
def _i0(x):
  abs_x = lax.abs(x)
  return lax.mul(lax.exp(abs_x), lax_special.bessel_i0e(abs_x))

