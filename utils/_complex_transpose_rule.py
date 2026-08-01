
def _complex_transpose_rule(t, x, y):
  assert ad.is_undefined_primal(x) or ad.is_undefined_primal(y)
  if ad.is_undefined_primal(x) and ad.is_undefined_primal(y):
    if type(t) is ad_util.Zero:
      return [ad_util.Zero(x.aval), ad_util.Zero(y.aval)]
    else:
      return [_unbroadcast(x.aval, real(t)), _unbroadcast(y.aval, imag(neg(t)))]
  elif ad.is_undefined_primal(x):
    if type(t) is ad_util.Zero:
      return [ad_util.Zero(x.aval), None]
    else:
      return [_unbroadcast(x.aval, real(t)), None]
  else:
    if type(t) is ad_util.Zero:
      return [None, ad_util.Zero(y.aval)]
    else:
      return [None, _unbroadcast(y.aval, imag(neg(t)))]

