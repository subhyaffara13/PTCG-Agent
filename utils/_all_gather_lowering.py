from typing import Any

def _all_gather_lowering(ctx, x, *, all_gather_dimension, axis_name,
                         axis_index_groups, axis_size, tiled,
                         platform=None, is_async=False):
  x_aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  if is_async:
    out_aval = out_aval.inner_aval
  axis_context = ctx.module_context.axis_context
  is_spmd = isinstance(axis_context, (SPMDAxisContext, ShardingContext))
  if not tiled:
    new_shape = list(x_aval.shape)
    new_shape.insert(all_gather_dimension, 1)
    broadcast_dimensions = [i for i in range(len(new_shape)) if i != all_gather_dimension]
    x = hlo.broadcast_in_dim(
        mlir.aval_to_ir_type(ctx.module_context, x_aval.update(shape=new_shape)), x,
        mlir.dense_int_array(broadcast_dimensions))
  replica_groups = _replica_groups(ctx.module_context.axis_context, axis_name,
                                    axis_index_groups)
  if is_spmd:
    # We want to emit the all-gather with global device IDs and a
    # channel ID, as otherwise it interprets the devices as replicas instead
    # of partitions - and XLA is configured with only a single replica.
    other_args: dict[str, Any] = dict(
        channel_handle=hlo.ChannelHandle.get(
            mlir.COLLECTIVE_CHANNEL_ID, mlir.DEVICE_TO_DEVICE_TYPE),
        use_global_device_ids=ir.BoolAttr.get(True))
  else:
    other_args = {}

  out_type = mlir.aval_to_ir_type(ctx.module_context, out_aval)
  if not is_async:
    return hlo.AllGatherOp(
        [out_type],
        [x], all_gather_dim=mlir.i64_attr(all_gather_dimension),
        replica_groups=_replica_groups_hlo(replica_groups),
        **other_args).results

  future_type = hlo.FutureType.get([out_type])
  async_start = hlo.AsyncStartOp(future_type, [x])
  block = async_start.regions[0].blocks.append(x.type)
  with ir.InsertionPoint(block):
    results = hlo.AllGatherOp(
        [out_type],
        [block.arguments[0]],
        all_gather_dim=mlir.i64_attr(all_gather_dimension),
        replica_groups=_replica_groups_hlo(replica_groups),
        **other_args,
    ).results
    hlo.return_(results)
  return async_start.results

