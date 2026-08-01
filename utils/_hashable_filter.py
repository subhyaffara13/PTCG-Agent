
def _hashable_filter(x):
  """Hashable version of CollectionFilter."""
  if isinstance(x, str):
    return (x,)
  if isinstance(x, Iterable):
    return tuple(x)  # convert un-hashable list & sets to tuple
  if isinstance(x, DenyList):
    return DenyList(
      _hashable_filter(x.deny)
    )  # convert inner filter recursively
  return x

