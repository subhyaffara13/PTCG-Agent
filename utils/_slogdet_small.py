
def _slogdet_small(a: Array) -> tuple[Array, Array]:
  """slogdet for n in {1, 2} using analytic formulas only (no solve)."""
  n = a.shape[-1]
  if n == 1:
    return _slogdet_1x1(a)
  elif n == 2:
    return _slogdet_2x2(a)
  else:
    raise ValueError(f"_slogdet_small only supports n in {{1, 2}}, got n={n}")

