
def _reduce_vma_rule(*avals, computation, jaxpr, dimensions):
  operand_avals, _ = split_list(avals, [len(avals) // 2])
  out_vma = core.standard_vma_rule('reduce', *operand_avals)
  return [out_vma] * len(operand_avals)

