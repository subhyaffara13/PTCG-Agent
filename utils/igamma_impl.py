
def igamma_impl(a, x, *, dtype):
  is_nan = bitwise_or(_isnan(a), _isnan(x))
  x_is_infinity = eq(x, _const(x, float('inf')))
  a_is_zero = eq(a, _const(a, 0))
  x_is_zero = eq(x, _const(x, 0))
  domain_error = _reduce(bitwise_or, [lt(x, _const(x, 0)), lt(a, _const(a, 0)), bitwise_and(a_is_zero, x_is_zero), is_nan])

  use_igammac = bitwise_and(ge(x, _const(x, 1)), gt(x, a))
  ax = a * log(x) - x - lgamma(a)
  underflow = lt(ax, -log(dtypes.finfo(dtype).max))
  ax = exp(ax)
  enabled = bitwise_not(_reduce(bitwise_or, [x_is_zero, domain_error, underflow, x_is_infinity]))

  output = select(
    use_igammac,
    _const(a, 1) -
      _igammac_continued_fraction(ax, x, a, bitwise_and(enabled, use_igammac),
                                  dtype, IgammaMode.VALUE),
    _igamma_series(ax, x, a, bitwise_and(enabled, bitwise_not(use_igammac)),
                   dtype, IgammaMode.VALUE)
  )
  output = select(x_is_zero, full_like(a, 0), output)
  output = select(x_is_infinity, full_like(a, 1), output)
  output = select(domain_error, full_like(a, float('nan')), output)
  return output

