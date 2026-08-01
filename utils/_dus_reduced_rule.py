
def _dus_reduced_rule(operand, update):
  if core.getr(operand) != core.getr(update):
    raise core.ShardingTypeError(
        "dynamic_update_slice operand and update must be reduced along the"
        " same axes. Got operand sharding"
        f" {operand.str_short(mesh_axis_types=True)} and update sharding"
        f" {update.str_short(mesh_axis_types=True)}.")
  return core.getr(operand)

