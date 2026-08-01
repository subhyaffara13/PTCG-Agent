
def _get_shape_from_index(slc: Index, shape: Shape) -> Shape:
  return tuple(
      (s.stop or dim) - (s.start or 0)
      for s, dim in safe_zip(slc, shape)
      if isinstance(s, slice)  # If element is int, this dimension is reduced
  )

