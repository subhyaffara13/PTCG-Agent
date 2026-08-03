from typing import Any

def _all_to_all_lowering(
    ctx, x, *, split_axis, concat_axis, axis_name, axis_index_groups, tiled,
    is_async=False
):
  del tiled  # expand_dims and squeeze is done in `all_to_all` if `True`
  # Workaround for AllToAll not being implemented on CPU.
  replica_groups = _replica_groups(ctx.module_context.axis_context, axis_name,
                                   axis_index_groups)
  if not is_async and len(replica_groups[0]) == 1:
    # TODO(mwhittaker): This optimization doesn't play well with async
    # collectives. Support it; or optimize it in XLA.
    return [x]
  split_count = len(replica_groups[0])
  if not all(split_count == len(g) for g in replica_groups):
    raise ValueError('Replica groups must be equally sized')
  is_spmd = isinstance(
      ctx.module_context.axis_context,
      (SPMDAxisContext, ShardingContext),
  )
  if is_spmd:
    # We want to emit the all-gather with global device IDs and a
    # channel ID, as otherwise it interprets the devices as replicas instead
    # of partitions - and XLA is configured with only a single replica.
    channel_handle = hlo.ChannelHandle.get(mlir.COLLECTIVE_CHANNEL_ID,
                                           mlir.DEVICE_TO_DEVICE_TYPE)
    other_args: dict[str, Any] = dict(channel_handle=channel_handle)
  else:
    other_args = {}

  if not is_async:
    return hlo.AllToAllOp(
        [x],
        split_dimension=mlir.i64_attr(split_axis),
        concat_dimension=mlir.i64_attr(concat_axis),
        split_count=mlir.i64_attr(split_count),
        replica_groups=_replica_groups_hlo(replica_groups),
        **other_args,
    ).results

  (out_aval,) = ctx.avals_out
  out_aval = out_aval.inner_aval
  # pyrefly: ignore[missing-attribute]
  future_type = hlo.FutureType.get([mlir.aval_to_ir_type(ctx.module_context, out_aval)])
  async_start = hlo.AsyncStartOp(future_type, [x])
  block = async_start.regions[0].blocks.append(x.type)
  with ir.InsertionPoint(block):
    results = hlo.AllToAllOp(
        [block.arguments[0]],
        split_dimension=mlir.i64_attr(split_axis),
        concat_dimension=mlir.i64_attr(concat_axis),
        split_count=mlir.i64_attr(split_count),
        replica_groups=_replica_groups_hlo(replica_groups),
        **other_args,
    ).results
    hlo.return_(results)
  return async_start.results

