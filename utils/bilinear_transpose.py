
def bilinear_transpose(lhs_rule, rhs_rule, cotangent, x, y, **kwargs):
  assert is_undefined_primal(x) ^ is_undefined_primal(y)
  if is_undefined_primal(x):
    if type(cotangent) is Zero:
      return Zero(x.aval.to_ct_aval()), None
    else:
      out = lhs_rule(cotangent, x, y, **kwargs)
      return out, None
  else:
    if type(cotangent) is Zero:
      return None, Zero(y.aval.to_ct_aval())
    else:
      out = rhs_rule(cotangent, x, y, **kwargs)
      return None, out

