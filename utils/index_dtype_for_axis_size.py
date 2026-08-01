
def index_dtype_for_axis_size(
    indices_dtype: DType,
    axis_size: DimSize,
    wrap_negative_indices: bool,
) -> DType:
  """Upcast indices_dtype if necessary to avoid overflow."""
  # The primary way we can overflow is negative index + axis_size if axis_size
  # is larger than indices_dtype max. For simplicity, though, we just upcast
  # whenever wrapping negative indices. This could be changed in the future.
  if not wrap_negative_indices:
    return indices_dtype
  return int_dtype_for_dim(axis_size, signed=True)

