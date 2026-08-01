
def _conj_transpose_rule(t, x, *, input_dtype):
  assert ad.is_undefined_primal(x)
  if type(t) is ad_util.Zero:
    return [ad_util.Zero(x.aval)]
  elif dtypes.issubdtype(input_dtype, np.complexfloating):
    return [conj(t)]
  else:
    return [real(t)]

