
def _split_weak_type_rule(operand, *, sizes, axis):
  return (operand.weak_type,) * len(sizes)

