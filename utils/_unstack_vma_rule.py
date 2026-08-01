
def _unstack_vma_rule(operand, *, axis):
  out_vma = core.standard_vma_rule('unstack', operand)
  return [out_vma] * operand.shape[axis]

