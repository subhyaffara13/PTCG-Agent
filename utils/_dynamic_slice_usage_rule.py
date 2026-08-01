
def _dynamic_slice_usage_rule(ctx, used_out: set[Usage], **params):
  del params
  if used_out == {Usage.SCALAR_PREFETCH}:
    raise NotImplementedError('scalar prefetch not supported yet')
  elif used_out == {Usage.REGULAR}:
    usage = [used_out] + [{Usage.SCALAR_PREFETCH}] * (len(ctx.avals_in) - 1)
    return usage
  else:
    return [set()] * len(ctx.avals_in)

