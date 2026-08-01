
def reduce_window_shape_tuple(operand_shape, window_dimensions, window_strides,
                              padding, base_dilation=None,
                              window_dilation=None):
  if base_dilation is not None:
    operand_shape = lax._dilate_shape(operand_shape, base_dilation)
  if window_dilation is not None:
    window_dimensions = lax._dilate_shape(window_dimensions, window_dilation)
  operand_padded = tuple(d + pl + ph for d, (pl, ph) in zip(operand_shape, padding))
  return tuple(map(core.stride_dim, operand_padded, window_dimensions, window_strides))

