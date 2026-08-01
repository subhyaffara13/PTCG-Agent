
def merge_lists(bs: Sequence[bool], l0: Sequence[T1], l1: Sequence[T2]
                ) -> list[T1 | T2]:
  """Merge the elements of two lists based on a mask."""
  assert sum(bs) == len(l1) and len(bs) - sum(bs) == len(l0)
  i0, i1 = iter(l0), iter(l1)
  out: list[T1 | T2] = [next(i1) if b else next(i0) for b in bs]
  sentinel = object()
  assert next(i0, sentinel) is next(i1, sentinel) is sentinel
  return out

