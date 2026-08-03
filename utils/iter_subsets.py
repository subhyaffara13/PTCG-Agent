import itertools

def iter_subsets(s: Sequence) -> Iterable[tuple]:
  """Return an iterator over all subsets of a sequence s"""
  return itertools.chain.from_iterable(
      itertools.combinations(s, n) for n in range(len(s) + 1)
  )

