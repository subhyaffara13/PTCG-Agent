
def _canonicalize_dimension(dim: DimSize) -> DimSize:
  # Dimensions are most commonly integral (by far), so we check that first.
  try:
    return operator.index(dim)
  except TypeError as e:
    type_error = e
  if is_dim(dim):
    return dim
  else:
    raise type_error

