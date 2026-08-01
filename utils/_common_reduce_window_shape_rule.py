
def _common_reduce_window_shape_rule(
    operand,
    window_dimensions,
    window_strides,
    padding,
    base_dilation,
    window_dilation,
):
  lax._check_shapelike("reduce_window", "window_dimensions", window_dimensions,
                       non_zero_shape=True)
  lax._check_shapelike("reduce_window", "window_strides", window_strides,
                       non_zero_shape=True)
  lax._check_shapelike("reduce_window", "base_dilation", base_dilation)
  lax._check_shapelike("reduce_window", "window_dilation", window_dilation)
  if operand.ndim != len(window_dimensions):
    msg = (
        "reduce_window got the wrong number of window_dimensions for "
        "operand: got operand shape {} with window_dimensions {}."
    )
    raise TypeError(msg.format(operand.shape, window_dimensions))
  if len(window_strides) != len(window_dimensions):
    msg = ("reduce_window got inconsistent window_strides and "
           "window_dimensions: got window_strides {} and window_dimensions {}.")
    raise TypeError(msg.format(window_strides, window_dimensions))
  if len(base_dilation) != len(window_dimensions):
    msg = ("reduce_window got inconsistent base_dilation and "
           "window_dimensions: got base_dilation {} and window_dimensions {}.")
    raise TypeError(msg.format(base_dilation, window_dimensions))
  if len(window_dilation) != len(window_dimensions):
    msg = ("reduce_window got inconsistent window_dilation and "
           "window_dimensions: got window_dilation {} and window_dimensions "
           "{}.")
    raise TypeError(msg.format(window_dilation, window_dimensions))

  return reduce_window_shape_tuple(operand.shape, window_dimensions,
                                   window_strides, padding, base_dilation,
                                   window_dilation)

