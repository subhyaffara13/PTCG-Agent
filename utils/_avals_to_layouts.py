
def _avals_to_layouts(avals) -> Sequence[Sequence[int]]:
  return [tuple(range(a.ndim - 1, -1, -1)) for a in avals]

