
def _sub_transpose(t, x, y):
  # Morally the following assertion is true, but see the comment in add_p's
  # transpose rule.
  # assert ad.is_undefined_primal(x) and ad.is_undefined_primal(y)
  x_aval = x.aval if ad.is_undefined_primal(x) else core.typeof(x)
  y_aval = y.aval if ad.is_undefined_primal(y) else core.typeof(y)
  if type(t) is ad_util.Zero:
    return [ad_util.Zero(x_aval), ad_util.Zero(y_aval)]
  else:
    return [_unbroadcast(x_aval, t), _unbroadcast(y_aval, neg(t))]

