
def _sin_complex(x):
  # use expm1 instead of exp to avoid cancellation when abs(x) is small
  # relies on the quality of real-valued expm1, sin, cos
  # sin(x) = complex(sin(real(x)) * cosh(imag(x)), cos(real(x)) * sinh(imag(x)))
  # 2 * sinh(x) = exp(x) - 1 - (exp(-x) - 1) = expm1(x) - expm1(-x)
  # 2 * cosh(x) = exp(x) - 1 + (exp(-x) - 1) + 2 = expm1(x) + expm1(-x) + 2
  a, b = real(x), imag(x)
  a_is_zero = eq(a, _const(a, 0))
  two = _const(a, 2)
  sn, cs = sin(a), cos(a)
  e1m, e2m = expm1(b), expm1(neg(b))
  snh, csh = div(sub(e1m, e2m), two), div(add(add(e1m, e2m), two), two)
  re, im = mul(sn, csh), mul(cs, snh)
  # avoid nan value when real(x) is zero and abs(x) is so large that abs(expm1(x)) is inf
  return select(a_is_zero, complex(_const(a, 0), im), complex(re, im))

