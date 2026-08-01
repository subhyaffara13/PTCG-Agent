
def _broadcast_shapes_uncached(*shapes: tuple[int, ...]):
  _validate_shapes(shapes)
  fst, *rst = shapes
  if not rst: return fst

  # First check if we need only rank promotion (and not singleton-broadcasting).
  result_shape = _max(shapes, key=len)
  ndim = len(result_shape)
  if ndim == 0 or all(core.definitely_equal_shape(result_shape[ndim - len(s):], s) for s in shapes):
    return result_shape

  # Next try singleton-broadcasting, padding out ranks using singletons.
  rank_promoted_shapes = tuple((*((1,) * (ndim - len(shape))), *shape) for shape in shapes)
  try:
    return _try_broadcast_shapes(*rank_promoted_shapes, name='broadcast_shapes')
  except TypeError as err:
    # Raise ValueError here for backward compatibility.
    raise ValueError(f"Incompatible shapes for broadcasting: shapes={list(shapes)}") from err

