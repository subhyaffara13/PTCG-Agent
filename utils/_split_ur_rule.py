
def _split_ur_rule(operand, *, sizes, axis):
  out_shapes = _split_shape_rule(operand, sizes=sizes, axis=axis)
  return [getu(operand)] * len(out_shapes), [getr(operand)] * len(out_shapes)

