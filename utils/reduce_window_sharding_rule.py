
def reduce_window_sharding_rule(operand, window_dimensions, window_strides,
                                padding, base_dilation, window_dilation):
  out_shape = reduce_window_shape_tuple(
      operand.shape, window_dimensions, window_strides, padding, base_dilation,
      window_dilation)
  return lax.slicing._get_sharding_for_varying_out_shape(
      out_shape, operand, 'reduce_window')

