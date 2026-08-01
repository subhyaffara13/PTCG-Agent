
def _get_spatial_valid_position_count(
    dnums: convolution.ConvDimensionNumbers,
    lhs: roofline.RooflineShape,
    rhs: roofline.RooflineShape,
    out: roofline.RooflineShape,
    window_strides: Sequence[int],
    padding: Sequence[tuple[int, int]],
    lhs_dilation: Sequence[int],
    rhs_dilation: Sequence[int],
) -> int:
  """Gets the number of valid spatial positions for conv_general_dilated.

  Args:
    dnums: The dimension numbers for the convolution.
    lhs: The shape of the left-hand side of the convolution.
    rhs: The shape of the right-hand side of the convolution.
    out: The shape of the output of the convolution.
    window_strides: The stride of the window along each spatial dimension.
    padding: The padding applied to the input along each spatial dimension.
    lhs_dilation: The dilation factor for the left-hand side along each spatial
      dimension.
    rhs_dilation: The dilation factor for the right-hand side along each spatial
      dimension.
  """
  input_spatial_dims, kernel_spatial_dims, out_spatial_dims = (
      dnums.lhs_spec[2:],
      dnums.rhs_spec[2:],
      dnums.out_spec[2:],
  )

  valid_position_counts = 1
  # Loop over each spatial dimension and determine how many valid positions
  # there are for each dimension.
  for d in range(len(input_spatial_dims)):
    valid_position_counts *= _get_spatial_valid_position_count_for_one_dim(
        window_dim_stride=window_strides[d],
        base_dilation=lhs_dilation[d],
        window_dilation=rhs_dilation[d],
        kernel_limit=rhs.shape[kernel_spatial_dims[d]],
        input_limit=lhs.shape[input_spatial_dims[d]],
        output_limit=out.shape[out_spatial_dims[d]],
        padding=padding[d],
    )

  return valid_position_counts

