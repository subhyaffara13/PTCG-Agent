
def canonicalize_axes(axes, ndim) -> tuple[int, ...]:
  """Vendored version of :func:`numpy.lib.array_utils.normalize_axis_tuple`.
  """
  return tuple(canonicalize_axis(x, ndim) for x in axes)

