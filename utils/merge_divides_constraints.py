import math


def merge_divides_constraints(d0: Divides, d1: Divides) -> Divides:
  if d0.expr != d1.expr:
    raise ValueError("Divides constraints must apply to the same expression.")
  # If the two tuples are of different lengths, the larger tuple will be
  # truncated to the length of the smaller tuple. This preserves the semantics
  # of the Divides constraints where a tiling's rank cannot exceed the size of
  # tiling_multiple.
  min_len = min(len(d0.tiling_multiple), len(d1.tiling_multiple))
  if min_len == 0:
    return Divides(d0.expr, ())
  tiling_multiple = []
  for t0, t1 in zip(d0.tiling_multiple[-min_len:], d1.tiling_multiple[-min_len:], strict=True):
    tiling_multiple.append(math.gcd(t0, t1))
  return Divides(d0.expr, tuple(tiling_multiple))

