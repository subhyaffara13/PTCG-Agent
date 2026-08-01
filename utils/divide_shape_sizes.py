
def divide_shape_sizes(s1: Shape, s2: Shape) -> DimSize:
  """Returns an integer "i" s.t., i * size(s2) == size(s1).
  Raises InconclusiveDimensionOperation if there is no such integer."""
  sz1 = math.prod(s1)
  sz2 = math.prod(s2)
  if definitely_equal(sz1, sz2):  # Takes care of sz1 and sz2 being 0
    return 1
  q, r = divmod(sz1, sz2)
  if isinstance(r, Tracer) or r != 0:
    raise InconclusiveDimensionOperation(
        f"Cannot divide evenly the sizes of shapes {tuple(s1)} and {tuple(s2)}. "
        f"The remainder {r} should be 0.")
  return q

