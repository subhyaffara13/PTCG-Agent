
def filter_to_set(x: Filter) -> set[str]:
  """Converts a Filter into a set of collections, fails on the infinite set.

  Args:
    x: a filter (boolean, string, or list of strings).

  Returns:
    The input filter represented as a set of strings.
  """
  assert x is not True and not isinstance(x, DenyList), 'Infinite set'
  if x is False:
    return set()
  if isinstance(x, str):
    return {x}
  if isinstance(x, typing.Collection):
    return set(x)
  raise errors.InvalidFilterError(x)

