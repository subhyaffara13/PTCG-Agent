
def _unstack_dtype_rule(operand, *, axis):
  num_results = operand.shape[axis]
  return (operand.dtype,) * num_results

