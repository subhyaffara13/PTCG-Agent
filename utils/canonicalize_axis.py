
def canonicalize_axis(axis, ndim):
  """Vendored version of :func:`numpy.lib.array_utils.normalize_axis_index`.
  """
  if 0 <= (axis := operator.index(axis)) < ndim:
    return axis
  elif -ndim <= axis < 0:
    return axis + ndim
  else:
    raise ValueError(f'axis {axis} is out of bounds for array of '
                     f'dimension {ndim}')


def canonicalize_axis(axis: SupportsIndex, num_dims: int) -> int:
  """Canonicalize an axis in [-num_dims, num_dims) to [0, num_dims)."""
  axis = operator.index(axis)
  if not -num_dims <= axis < num_dims:
    raise ValueError(f"axis {axis} is out of bounds for array of dimension {num_dims}")
  if axis < 0:
    axis = axis + num_dims
  return axis

