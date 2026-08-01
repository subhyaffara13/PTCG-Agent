
def _squeeze_transpose_rule(t, operand, *, dimensions):
  assert ad.is_undefined_primal(operand)
  return [expand_dims(t, dimensions)]

