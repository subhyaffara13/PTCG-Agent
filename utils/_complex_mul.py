
def _complex_mul(mul, x, y):
  # We use a trick for complex multiplication sometimes attributed to Gauss
  # which uses three multiplications and five additions; instead of the naive
  # method of four multiplications and two additions.
  # https://en.wikipedia.org/wiki/Multiplication_algorithm#Complex_multiplication_algorithm
  #
  # This performance win comes with a trade-off in accuracy; especially in
  # cases when the real and imaginary differ hugely in magnitude. The relative
  # error bound (e.g. 1p-24 in case of float32) would be relative to the
  # maximum of real and imaginary parts of the result instead of being
  # satisfied by the real and imaginary parts independently of each other.
  x_re, x_im = lax.real(x), lax.imag(x)
  y_re, y_im = lax.real(y), lax.imag(y)
  k1 = mul(lax.add(x_re, x_im), y_re)
  k2 = mul(x_re, lax.sub(y_im, y_re))
  k3 = mul(x_im, lax.add(y_re, y_im))
  return lax.complex(lax.sub(k1, k3), lax.add(k1, k2))

