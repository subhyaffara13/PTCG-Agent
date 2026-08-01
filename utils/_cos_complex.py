
def _cos_complex(x):
  # cos(x) = complex(cos(real(x)) * cosh(imag(x)), -sin(real(x)) * sinh(imag(x)))
  # see also _sin_complex
  a, b = real(x), imag(x)
  a_is_zero = eq(a, _const(a, 0))
  two = _const(a, 2)
  sn, cs = sin(a), cos(a)
  e1m, e2m = expm1(b), expm1(neg(b))
  snh, csh = div(sub(e1m, e2m), two), div(add(add(e1m, e2m), two), two)
  re, im = mul(cs, csh), mul(neg(sn), snh)
  return select(a_is_zero, complex(re, _const(a, 0)), complex(re, im))

