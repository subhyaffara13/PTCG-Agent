
def cmp_sequence(s1, s2, elem_cmp) -> int:
  """Compares two sequences using `elem_cmp`."""
  l2 = len(s2)
  for i, e1 in enumerate(s1):
    if i >= l2: return 1
    if c := elem_cmp(e1, s2[i]): return c
  if len(s1) < l2: return -1
  return 0

