
def split_list_checked(args: Sequence[T], ns: Sequence[int]) -> list[list[T]]:
  """Split list into sublists of the specified sizes."""
  args = list(args)
  assert sum(ns) == len(args) and all(n >= 0 for n in ns)
  lists = []
  for n in ns:
    lists.append(args[:n])
    args = args[n:]
  return lists

