
def _add_transpose(t, x, y):
  # Morally the following assertion is true, but because we instantiate zeros in
  # some places (e.g. in custom_jvp) it may not always hold. For example, see
  # api_test.py's CustomJVPTest.test_jaxpr_zeros.
  # assert ad.is_undefined_primal(x) and ad.is_undefined_primal(y)
  x_aval = x.aval if ad.is_undefined_primal(x) else core.typeof(x).to_ct_aval()
  y_aval = y.aval if ad.is_undefined_primal(y) else core.typeof(y).to_ct_aval()
  if type(t) is ad_util.Zero:
    return [ad_util.Zero(x_aval), ad_util.Zero(y_aval)]
  else:
    return [_unbroadcast(x_aval, t), _unbroadcast(y_aval, t)]

