
def _compatible(shape1: Sequence[int], shape2: Sequence[int]) -> bool:
  return all(s1 in (1, s2) for s1, s2 in safe_zip(shape1, shape2))

