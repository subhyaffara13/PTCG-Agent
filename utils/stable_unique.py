
def stable_unique(it: Iterable[T]) -> Iterable[T]:
  """Returns unique elements from `it` in the order of occurrence.

  The elements must be hashable.
  """
  return dict.fromkeys(it).keys()

