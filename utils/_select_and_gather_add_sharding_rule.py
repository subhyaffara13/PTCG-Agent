
def _select_and_gather_add_sharding_rule(
    tangents, operand, *, select_prim, window_dimensions, window_strides,
    padding, base_dilation, window_dilation):
  if tangents.sharding != operand.sharding:
    raise core.ShardingTypeError(
        "select_and_gather_add tangents and operand shardings must match, "
        f"got {tangents.sharding} and {operand.sharding}.")
  return reduce_window_sharding_rule(
      operand, window_dimensions, window_strides, padding, base_dilation,
      window_dilation)

