
def subvals(lst: Sequence[T], replace: Iterable[tuple[int, T]]) -> tuple[T, ...]:
  """Substitute values within a list."""
  lst = list(lst)
  for i, v in replace:
    lst[i] = v
  return tuple(lst)

