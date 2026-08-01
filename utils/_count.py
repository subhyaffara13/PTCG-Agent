
def _count(
    a: ArrayLike,
    axis: Axis,
    keepdims: bool,
    where: ArrayLike | None,
    dtype: DTypeLike,
):
  if where is None:
    if axis is None:
      count = core.dimension_as_value(np.size(a))
    else:
      count = core.dimension_as_value(_axis_size(a, axis))
    count = lax.convert_element_type(count, dtype)
  else:
    count = sum(_broadcast_to(where, np.shape(a)), axis, dtype=dtype, keepdims=keepdims)
  return count

