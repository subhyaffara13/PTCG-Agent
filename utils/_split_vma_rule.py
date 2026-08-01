
def _split_vma_rule(operand, *, sizes, axis):
  out_vma = core.standard_vma_rule('split', operand)
  out_shapes = _split_shape_rule(operand, sizes=sizes, axis=axis)
  return [out_vma] * len(out_shapes)

