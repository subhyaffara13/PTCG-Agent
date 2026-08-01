
def _unstack_ur_rule(operand, *, axis):
  return [getu(operand)] * operand.shape[axis], [getr(operand)] * operand.shape[axis]

