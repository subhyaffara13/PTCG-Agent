
def _bitcast_batch_rule(batched_args, batch_axes, *, ty):
  return bitcast(*batched_args, ty=ty), batch_axes[0]

