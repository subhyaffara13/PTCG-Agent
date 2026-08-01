
def _dynamic_update_slice_sharding_rule(operand, update, *start_indices):
  if operand.sharding != update.sharding:
    raise core.ShardingTypeError(
        "dynamic_update_slice operand sharding must be equal to update"
        " sharding, got operand sharding"
        f" {operand.str_short(mesh_axis_types=True)} and update sharding"
        f" {update.str_short(mesh_axis_types=True)}.")
  return operand.sharding

