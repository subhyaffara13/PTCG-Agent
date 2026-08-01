
def partition_list(choice, lst):
  out = [], []
  which = [out[choice(elt)].append(elt) or choice(elt) for elt in lst]
  def merge(l1, l2):
    i1, i2 = iter(l1), iter(l2)
    return [next(i2 if snd else i1) for snd in which]
  return out, merge


def partition_list(bs: Sequence[bool], l: Sequence[T]) -> tuple[list[T], list[T]]:
  """Partition a list into two based on a mask."""
  assert len(bs) == len(l)
  lists: tuple[list[T], list[T]] = ([], [])
  for b, x in zip(bs, l):
    lists[b].append(x)
  return lists

