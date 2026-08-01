
def _select_and_scatter_sharding_rule(
    operand, source, init_value, *, select_jaxpr, select_consts, scatter_jaxpr,
    scatter_consts, window_dimensions, window_strides, padding):
  return operand.sharding

