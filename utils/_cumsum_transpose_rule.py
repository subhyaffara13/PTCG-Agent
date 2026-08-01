
def _cumsum_transpose_rule(t, operand, *, axis: int, reverse: bool):
  return [cumsum(t, axis=axis, reverse=not reverse)]

