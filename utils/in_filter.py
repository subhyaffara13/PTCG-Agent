
def in_filter(filter_like: Filter, col: str) -> bool:
  """Checks whether a filter can be applied to a collection.

  Used for both collections and rng sequence filters.

  Args:
    filter_like: a filter (either a boolean, a string, or a list of strings) for
      a collection.
    col: a collection, which is a string identifying a dictionary of data, for
      instance "params" or "batch_stats".

  Returns:
    True if either `filter_like` is True, equal to `col`, or a sequence
    containing `col`.
  """
  if isinstance(filter_like, str):
    return col == filter_like
  if isinstance(filter_like, typing.Collection):
    return col in filter_like
  if isinstance(filter_like, bool):
    return filter_like
  if isinstance(filter_like, DenyList):
    return not in_filter(filter_like.deny, col)
  raise errors.InvalidFilterError(filter_like)

