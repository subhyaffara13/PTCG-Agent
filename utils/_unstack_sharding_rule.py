
def _unstack_sharding_rule(operand, *, axis):
  if operand.sharding.spec[axis] is not None:
    raise core.ShardingTypeError(
        f"unstack operand cannot be sharded on the unstacking axis {axis}. "
        f"Got operand type={operand.str_short(True)}"
    )
  out_shapes = _unstack_shape_rule(operand, axis=axis)
  new_spec = list(operand.sharding.spec)
  new_spec.pop(axis)
  out_sharding = operand.sharding.update(
    spec=operand.sharding.spec.update(partitions=tuple(new_spec)))
  return [out_sharding] * len(out_shapes)

