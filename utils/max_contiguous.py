
def max_contiguous(x, values):
  """A compiler hint that asserts the ``values`` first values of ``x`` are contiguous."""
  if not isinstance(values, (list, tuple)):
    values = (values,)
  return max_contiguous_p.bind(x, values=tuple(values))

