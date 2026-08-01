
def to_predicate(filter: Filter) -> Predicate:
  """Converts a Filter to a predicate function.
  See `Using Filters <https://flax.readthedocs.io/en/latest/guides/filters_guide.html>`__.
  """

  if isinstance(filter, str):
    return WithTag(filter)
  elif isinstance(filter, type):
    return OfType(filter)
  elif isinstance(filter, bool):
    if filter:
      return Everything()
    else:
      return Nothing()
  elif filter is Ellipsis:
    return Everything()
  elif filter is None:
    return Nothing()
  elif callable(filter):
    return filter
  elif isinstance(filter, (list, tuple)):
    return Any(*filter)
  else:
    raise TypeError(f'Invalid collection filter: {filter:!r}. ')

