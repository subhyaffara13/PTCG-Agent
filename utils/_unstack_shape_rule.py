
def _unstack_shape_rule(operand, *, axis):
  if operand.ndim == 0:
    msg = "unstack requires arrays with rank > 0, however a scalar array of shape {} was passed."
    raise ValueError(msg.format(operand.shape))
  shape = list(operand.shape)
  num_results = shape.pop(axis)
  return (tuple(shape),) * num_results

