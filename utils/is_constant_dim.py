
def is_constant_dim(d: DimSize) -> bool:
  # Whether the dimension is a static integer constant.
  # Try using a fast path for non-concrete Tracers.
  if isinstance(d, Tracer) and not is_concrete(d):
    return False
  try:
    operator.index(d)
    return True
  except:
    return False

