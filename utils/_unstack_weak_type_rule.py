
def _unstack_weak_type_rule(operand, *, axis):
  num_results = operand.shape[axis]
  return (operand.weak_type,) * num_results

