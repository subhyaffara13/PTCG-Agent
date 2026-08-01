
def canonicalize_axis_tuple(axis: int | Sequence[int] | None, ndim: int, allow_duplicate: bool = False) -> tuple[int, ...]:
  if axis is None:
    return tuple(range(ndim))
  if isinstance(axis, Sequence):
    axis = tuple(canonicalize_axis(i, ndim) for i in axis)
    if not allow_duplicate and len(set(axis)) != len(axis):
      raise ValueError(f"repeated axis: {axis}")
    return axis
  else:
    return (canonicalize_axis(axis, ndim),)

