
def _argminmax_shape_rule(operand, *, axes, index_dtype):
  axis, = axes
  if not (0 <= axis < len(operand.shape)):
    raise ValueError(f"Invalid axis {axis} for operand shape {operand.shape}")
  if operand.shape[axis] < 1:
    raise ValueError("argmin and argmax require non-empty reduced dimension. "
                     f"operand.shape={operand.shape} {axis=}")
  return util.tuple_delete(operand.shape, axis)

