
def _is_reduction_signed(kind: vector.CombiningKind) -> bool | None:
  if kind in (vector.CombiningKind.MAXSI, vector.CombiningKind.MINSI):
    return True
  if kind in (vector.CombiningKind.MAXUI, vector.CombiningKind.MINUI):
    return False
  return None

