
def enumerate_negative(elems: Sequence[T]) -> Iterable[tuple[int, T]]:
  """Like built-in enumerate, but returns negative indices into the sequence."""
  offset = len(elems)
  for i, e in enumerate(elems):
    yield i - offset, e

