
def _reduce_logical_shape_rule(operand, *, axes):
  if operand.dtype != np.bool_ and not np.issubdtype(operand.dtype, np.integer):
    raise TypeError(f"logical reduction requires operand dtype bool or int, got {operand.dtype}.")
  return tuple(np.delete(operand.shape, axes))

