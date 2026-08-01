
def subtract_filters(a: Filter, b: Filter) -> Filter:
  """Returns the subtraction of b from a.

  Args:
    a: a filter.
    b: a filter.

  Returns:
    A filter matching with values in a that are not in b.
  """
  if b is True:
    return False
  if a is True:
    return DenyList(b)
  if isinstance(a, DenyList) and isinstance(b, DenyList):
    return subtract_filters(b.deny, a.deny)
  if isinstance(a, DenyList):
    return DenyList(union_filters(a.deny, b))
  if isinstance(b, DenyList):
    return intersect_filters(a, b.deny)
  a = filter_to_set(a)
  b = filter_to_set(b)
  return a - b

