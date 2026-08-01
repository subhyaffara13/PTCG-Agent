
def _calculate_conv_flops(
    lhs: roofline.RooflineShape,
    rhs: roofline.RooflineShape,
    out: roofline.RooflineShape,
    window_strides: Sequence[int],
    padding: Sequence[tuple[int, int]],
    lhs_dilation: Sequence[int],
    rhs_dilation: Sequence[int],
    dimension_numbers: convolution.ConvGeneralDilatedDimensionNumbers,
    batch_group_count: int,
) -> int:
  """Calculates roofline unfused flops for Jax's conv_general_dilated primitive.

  See `jax.lax.conv_general_dilated` for details on the arguments.
  """
  dnums = convolution.conv_dimension_numbers(
      lhs.shape, rhs.shape, dimension_numbers
  )

  spatial_valid_position_counts = _get_spatial_valid_position_count(
      dnums, lhs, rhs, out, window_strides, padding, lhs_dilation, rhs_dilation
  )

  batch = lhs.shape[dnums.lhs_spec[0]]
  num_output_features = out.shape[dnums.out_spec[1]]
  num_input_features = rhs.shape[dnums.rhs_spec[1]]
  num_output_batch = batch / batch_group_count

  non_spatial_dims_factor = (
      num_input_features * num_output_features * num_output_batch
  )

  fma_count = non_spatial_dims_factor * spatial_valid_position_counts
  flops = fma_count * _FMA_FLOPS_FACTOR
  return int(flops)

