
def is_trivial_index(idx, shape) -> bool:
  """Checks if the index selects the entire shape."""

  # Slices that select the entire dimension.
  def _slices(d):
    slices = [slice(b, e, s) for b, e, s in it.product([0, None], [d, None], [1, None])]
    return [indexing.Slice(0, d, 1), *slices]

  if isinstance(idx, tuple):
    return all(i in _slices(d) for d, i in zip(shape, idx))

  return idx is ... or (len(shape) == 1 and idx in _slices(shape[0]))

