
def _div_transpose_rule(cotangent, x, y):
  assert ad.is_undefined_primal(x)
  if ad.is_undefined_primal(y):
    raise RuntimeError("nonlinear div can't be transposed")
  if type(cotangent) is ad_util.Zero:
    return [ad_util.Zero(x.aval), None]
  else:
    return [_unbroadcast(x.aval, div(cotangent, y)), None]

