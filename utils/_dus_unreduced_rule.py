
def _dus_unreduced_rule(operand, update):
  if core.getu(operand) != core.getu(update):
    raise core.ShardingTypeError(
        "dynamic_update_slice operand and update must be unreduced along the"
        " same axes. Got operand sharding"
        f" {operand.str_short(mesh_axis_types=True)} and update sharding"
        f" {update.str_short(mesh_axis_types=True)}.")
  return core.getu(operand)

