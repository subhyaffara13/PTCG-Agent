
def is_filter_empty(filter_like: Filter) -> bool:
  """Returns True if `filter_like` is an empty filter.

  Args:
    filter_like: The filter to test.

  Returns:
    A filter is empty when it is an empty collection, it is a bool with value
    False, ir it is a DenyList that matches everything. A string filter is never
    empty.
  """
  if isinstance(filter_like, str):
    return False
  if isinstance(filter_like, typing.Collection):
    return not filter_like
  if isinstance(filter_like, bool):
    return not filter_like
  if isinstance(filter_like, DenyList):
    # if any arbitrary collection is in the denylist it matches everything so
    # the filter is empty. This is checked with a stub.
    return in_filter(filter_like.deny, '__flax_internal_stub__')
  raise errors.InvalidFilterError(filter_like)

