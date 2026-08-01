
def _pbroadcast_lowering(ctx, x, *, axis_name, source):
  replica_groups = _replica_groups(ctx.module_context.axis_context, axis_name, None)
  def source_to_front(group):
    return [group[source]] + list(group[:source]) + list(group[source + 1:])
  replica_groups = [source_to_front(group) for group in replica_groups]
  is_spmd = isinstance(
      ctx.module_context.axis_context,
      (SPMDAxisContext, ShardingContext),
  )
  if is_spmd:
    # We want to emit the collective-broadcast with global device IDs and a
    # channel ID, as otherwise it interprets the devices as replicas instead
    # of partitions - and XLA is configured with only a single replica.
    channel_handle = hlo.ChannelHandle.get(mlir.COLLECTIVE_CHANNEL_ID,
                                           mlir.DEVICE_TO_DEVICE_TYPE)
    other_args: dict[str, Any] = dict(channel_handle=channel_handle)
  else:
    other_args = {}
  return hlo.CollectiveBroadcastOp(
      x, replica_groups=_replica_groups_hlo(replica_groups), **other_args
  ).results

