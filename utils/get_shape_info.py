
def get_shape_info(
    dtype: np.dtype,
    dimensions: Sequence[int],
) -> Mapping[str, Sequence[int] | str]:
  """Returns shape info in the format expected by read requests."""
  return {
      "xla_primitive_type_str": dtype_to_xla_primitive_type_str(dtype),
      "dimensions": dimensions,
  }

