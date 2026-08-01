
def _slice_ur_rule(operand, *, start_indices, limit_indices, strides):
  return core.getu(operand), core.getr(operand)

