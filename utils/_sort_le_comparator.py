
def _sort_le_comparator(*operands, num_keys=1):
  x_keys, y_keys = _operands_to_keys(*operands, num_keys=num_keys)
  p: Array | None = None
  for xk, yk in zip(x_keys[::-1], y_keys[::-1]):
    xk, yk = core.auto_insert_reshard(xk, yk)
    p = (bitwise_or(lt_to_p.bind(xk, yk), bitwise_and(eq_to_p.bind(xk, yk), p)) if p is not None
         else le_to_p.bind(xk, yk))
  return p

