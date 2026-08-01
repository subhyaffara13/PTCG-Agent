
def slice_shape(xs: NdSlice) -> Shape:
  """Calculates the shape of the given slice."""
  return tuple((s.stop - s.start + (s.step - 1)) // s.step for s in xs)

