
def _split_dtype_rule(operand, *, sizes, axis):
  return (operand.dtype,) * len(sizes)

