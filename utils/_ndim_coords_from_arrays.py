
def _ndim_coords_from_arrays(points, ndim=None):
  """Convert a tuple of coordinate arrays to a (..., ndim)-shaped array."""
  if isinstance(points, tuple) and len(points) == 1:
    # handle argument tuple
    points = points[0]
  if isinstance(points, tuple):
    p = broadcast_arrays(*points)
    for p_other in p[1:]:
      if p_other.shape != p[0].shape:
        raise ValueError("coordinate arrays do not have the same shape")
    points = empty(p[0].shape + (len(points),), dtype=float)
    for j, item in enumerate(p):
      points = points.at[..., j].set(item)
  else:
    check_arraylike("_ndim_coords_from_arrays", points)
    points = asarray(points)  # SciPy: asanyarray(points)
    if points.ndim == 1:
      if ndim is None:
        points = points.reshape(-1, 1)
      else:
        points = points.reshape(-1, ndim)
  return points

