
def _axis_size(
    axis_name: AxisName,
    axis_index_groups: Sequence[Sequence[int]] | None = None,
    /,
) -> int:
  axis_index_groups = _canonicalize_axis_index_groups(axis_index_groups)
  return psum(1, axis_name, axis_index_groups=axis_index_groups)


def _axis_size(a: ArrayLike, axis: int | Sequence[int]):
  if not isinstance(axis, Sequence):
    axes = (axis,)
  else:
    axes = axis
  size = 1
  a_shape = np.shape(a)
  for a in axes:
    size *= maybe_named_axis(a, lambda i: a_shape[i], lax_parallel.axis_size)
  return size

