
def _stack_shape_rule(*operands, axis):
  if not operands:
    msg = "stack expects at least one operand, got 0."
    raise ValueError(msg)
  if len({op.ndim for op in operands}) != 1:
    msg = "Cannot stack arrays with different numbers of dimensions: got {}."
    raise ValueError(msg.format(", ".join(str(o.shape) for o in operands)))
  if len({op.shape for op in operands}) != 1:
    msg = "All input arrays must have the same shape. Got {}."
    raise ValueError(msg.format(", ".join(str(o.shape) for o in operands)))

  shape = list(operands[0].shape)
  shape.insert(axis, len(operands))
  return tuple(shape)

