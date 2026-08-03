from typing import Any

def _pcollectives_lowering_common(ctx, *, axis_name, perm, op_name):
  replica_groups = _replica_groups(ctx.module_context.axis_context, axis_name, None)
  group_size = len(replica_groups[0])
  srcs, dsts = unzip2((src % group_size, dst % group_size) for src, dst in perm)
  if not (len(srcs) == len(set(srcs)) and len(dsts) == len(set(dsts))):
    msg = f"{op_name} sources and destinations must be unique, got {{}}."
    raise ValueError(msg.format(perm))

  full_perm = np.zeros((len(replica_groups), len(perm), 2), np.int64)
  for i, grp in enumerate(replica_groups):
    grp = sorted(grp)
    for j, (src, dst) in enumerate(perm):
      full_perm[i, j, 0] = grp[src]
      full_perm[i, j, 1] = grp[dst]
  full_perm = full_perm.reshape((-1, 2))

  axis_context = ctx.module_context.axis_context
  is_manual = (
      isinstance(axis_context, SPMDAxisContext)
      and axis_context.manual_axes
  )
  if is_manual:
    other_args: dict[str, Any] = dict(
        channel_handle=hlo.ChannelHandle.get(
            mlir.COLLECTIVE_CHANNEL_ID, mlir.DEVICE_TO_DEVICE_TYPE
        )
    )
  else:
    other_args = {}
  return full_perm, other_args

