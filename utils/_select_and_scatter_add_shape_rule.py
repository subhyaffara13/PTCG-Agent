
def _select_and_scatter_add_shape_rule(
    source, operand, *, select_prim, window_dimensions, window_strides,
    padding):
  return operand.shape

