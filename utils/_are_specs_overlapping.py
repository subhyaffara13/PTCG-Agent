
def _are_specs_overlapping(lhs, rhs):
  if lhs is None or rhs is None:
    return False
  lhs = (lhs,) if isinstance(lhs, str) else lhs
  rhs = (rhs,) if isinstance(rhs, str) else rhs
  return not set(lhs).isdisjoint(rhs)

