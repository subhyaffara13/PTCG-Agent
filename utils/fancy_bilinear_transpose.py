
def fancy_bilinear_transpose(lhs_rule, rhs_rule, cotangent, x, y, **kwargs):
  assert isinstance(x, GradAccum) ^ isinstance(y, GradAccum), (x, y)
  if isinstance(x, GradAccum):
    if type(cotangent) is not Zero and not isinstance(x, NullAccum):
      x.accum(lhs_rule(cotangent, x, y, **kwargs))
  else:
    if type(cotangent) is not Zero and not isinstance(y, NullAccum):
      y.accum(rhs_rule(cotangent, x, y, **kwargs))

