
def _dot_general_validated_shape(
    lhs_shape: tuple[int, ...], rhs_shape: tuple[int, ...],
    dimension_numbers: DotDimensionNumbers) -> tuple[int, ...]:
  """Validate the inputs and return the output shape."""
  lhs = core.ShapedArray(lhs_shape, np.float32)
  rhs = core.ShapedArray(rhs_shape, np.float32)
  return _dot_general_shape_rule(
    lhs, rhs, dimension_numbers=dimension_numbers,
    precision=None, preferred_element_type=None, out_sharding=None)

