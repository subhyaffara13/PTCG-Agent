
def igammac_impl(a, x, *, dtype):
  is_nan = bitwise_or(_isnan(a), _isnan(x))
  a_is_zero = eq(a, _const(a, 0))
  x_is_zero = eq(x, _const(x, 0))
  x_is_infinity = eq(x, _const(x, float('inf')))
  domain_error = _reduce(bitwise_or, [lt(x, _const(x, 0)), lt(a, _const(a, 0)), bitwise_and(a_is_zero, x_is_zero), is_nan])
  use_igamma = bitwise_or(lt(x, _const(x, 1)), lt(x, a))
  ax = a * log(x) - x - lgamma(a)
  underflow = lt(ax, -log(dtypes.finfo(dtype).max))
  enabled = bitwise_not(_reduce(bitwise_or, [domain_error, underflow, x_is_infinity, a_is_zero]))
  ax = exp(ax)

  igamma_call = _igamma_series(ax, x, a, bitwise_and(enabled, use_igamma),
                               dtype, IgammaMode.VALUE)
  igammac_cf_call = _igammac_continued_fraction(ax, x, a,
    bitwise_and(enabled, bitwise_not(use_igamma)), dtype, IgammaMode.VALUE)

  output = select(use_igamma, _const(a, 1) - igamma_call, igammac_cf_call)
  output = select(bitwise_or(x_is_infinity, a_is_zero), full_like(output, 0), output)
  output = select(domain_error, full_like(a, float('nan')), output)
  return output

