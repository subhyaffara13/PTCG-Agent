
def _select_and_scatter_add_sharding_rule(
    source, operand, *, select_prim, window_dimensions, window_strides,
    padding):
  return operand.sharding

