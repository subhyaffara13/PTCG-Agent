
def intersect_filters(a: Filter, b: Filter) -> Filter:
  """Take the intersection of two filters (similar to a logical and).

  Args:
    a: a filter.
    b: a filter.

  Returns:
    The intersection of the two input filters. For instance,
    `intersect_filters('f1', ['f1', 'f2']) = {'f1'}`.
  """
  if a is True:
    return b
  if b is True:
    return a
  if isinstance(a, DenyList) and isinstance(b, DenyList):
    return DenyList(union_filters(b.deny, a.deny))
  if isinstance(b, DenyList):
    b, a = a, b
  if isinstance(a, DenyList):
    return subtract_filters(b, a.deny)
  a = filter_to_set(a)
  b = filter_to_set(b)
  return a.intersection(b)

