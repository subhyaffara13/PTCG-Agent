
def _slice_as_tuple(s: slice):
  assert s.step is None
  return (s.start, s.stop)

