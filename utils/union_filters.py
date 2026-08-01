
def union_filters(a: Filter, b: Filter) -> Filter:
  """Takes the union of two filters (similar to a logical or).

  Args:
    a: a filter.
    b: a filter.

  Returns:
    The union of the two input filters. For instance,
    `union_filters('f1', ['f2']) = {'f1', 'f2'}`.
  """
  if a is True or b is True:
    return True
  if isinstance(a, DenyList) and isinstance(b, DenyList):
    return DenyList(intersect_filters(a.deny, b.deny))
  if isinstance(b, DenyList):
    a, b = b, a
  if isinstance(a, DenyList):
    return DenyList(subtract_filters(a.deny, b))

  a = filter_to_set(a)
  b = filter_to_set(b)
  return a.union(b)

