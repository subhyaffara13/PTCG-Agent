
def igamma_grad_a_impl(a, x, *, dtype):
  is_nan = bitwise_or(_isnan(a), _isnan(x))
  x_is_zero = eq(x, full_like(x,0))
  domain_error = bitwise_or(lt(x, full_like(x, 0)), le(a, full_like(a, 0)))
  use_igammac = bitwise_and(gt(x, full_like(x,1)), gt(x, a))
  ax = a * log(x) - x - lgamma(a)
  underflow = lt(ax, -log(dtypes.finfo(dtype).max))
  ax = exp(ax)
  enabled = bitwise_not(bitwise_or(bitwise_or(bitwise_or(
      x_is_zero, domain_error), underflow), is_nan))
  output = select(use_igammac,
    -_igammac_continued_fraction(ax, x, a, bitwise_and(enabled, use_igammac),
                                 dtype, IgammaMode.DERIVATIVE),
    _igamma_series(ax, x, a, bitwise_and(enabled, bitwise_not(use_igammac)),
                   dtype, IgammaMode.DERIVATIVE))
  output = select(x_is_zero, full_like(output,0), output)
  output = select(bitwise_or(domain_error, is_nan),
                  full_like(a, float('nan')), output)
  return output

