
def _get_spatial_valid_position_count_for_one_dim(
    window_dim_stride: int,
    base_dilation: int,
    window_dilation: int,
    kernel_limit: int,
    input_limit: int,
    output_limit: int,
    padding: tuple[int, int],
) -> int:
  """Gets the valid position count for conv for a single spatial dimension.

  Args:
    window_dim_stride: The stride of the window along this dimension.
    base_dilation: The base dilation factor along this dimension.
    window_dilation: The window dilation factor along this dimension.
    kernel_limit: The size of the kernel along this dimension.
    input_limit: The size of the input along this dimension.
    output_limit: The size of the output along this dimension.
    padding: The padding applied to the input along this dimension.
  """
  padding_low = padding[0]
  padding_high = padding[1]

  # These two conditions will create an N^2 iteration pattern with only N
  # valid elements. This is a performance optimization and produces the same
  # result as the whole loop.
  if (
      input_limit == output_limit
      and kernel_limit == output_limit
      and input_limit == base_dilation
      and window_dilation == 1
      and max(1, input_limit - 1) == window_dim_stride
      and padding_low == 0
      and padding_high == 0
  ):
    return input_limit

  if (
      input_limit == 1
      and kernel_limit == output_limit
      and window_dilation == 1
      and base_dilation == 1
      and window_dim_stride == 1
      and padding_low == output_limit - 1
      and padding_high == output_limit - 1
  ):
    return output_limit

  valid_position_count = 0
  # Loop over each point in the kernel
  for kernel_idx in range(kernel_limit):

    # Skip loop for trivial stride and base_dilation
    if window_dim_stride == 1 and base_dilation == 1:
      undilated_index_base = padding_low - kernel_idx * window_dilation
      upper_limit = min(
          input_limit + undilated_index_base,
          output_limit,
      )
      lower_limit = max(0, undilated_index_base)

      valid_position_count += max(upper_limit - lower_limit, 0)
      continue

    # Loop over each point in the output
    for output_idx in range(output_limit):
      # Calculate lhs (input) index without taking base dilation into account
      undilated_index = (
          output_idx * window_dim_stride
          - padding_low
          + kernel_idx * window_dilation
      )
      # Calculate the actual lhs (input) index after dilation
      lhs_spatial_index = int(undilated_index / base_dilation)

      # Skip if the lhs (input) index is to be dilated.
      if undilated_index != lhs_spatial_index * base_dilation:
        continue
      # Skip if input index is not in bound.
      if lhs_spatial_index < 0 or lhs_spatial_index >= input_limit:
        continue

      valid_position_count += 1
  return valid_position_count

