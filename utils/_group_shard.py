
def _group_shard(
    ctx,
    x: ir.Value,
    y: ir.Value,
    x_aval_out: core.AbstractValue,
    y_aval_out: core.AbstractValue,
) -> tuple[ir.Value, ir.Value]:
  shard_group_id = next(_next_shard_group_id)

  if config.use_shardy_partitioner.value:
    dialects.sdy.sharding_group(x, shard_group_id)
    dialects.sdy.sharding_group(y, shard_group_id)
    return x, y

  unknown_op_sharding = xc.OpSharding()
  unknown_op_sharding.type = xc.OpSharding.Type.UNKNOWN
  unknown_op_sharding.is_shard_group = True
  unknown_op_sharding.shard_group_id = shard_group_id
  unknown_op_sharding.shard_group_type = xc.OpSharding.ShardGroupType.AS

  x = mlir.wrap_with_sharding_op(ctx, x, x_aval_out, unknown_op_sharding,
                                 has_side_effect=True)
  y = mlir.wrap_with_sharding_op(ctx, y, y_aval_out, unknown_op_sharding,
                                 has_side_effect=True)
  return x, y

