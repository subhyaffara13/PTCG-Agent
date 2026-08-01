
def _broadcast_in_dim_usage_rule(ctx, used_out: set[Usage], **params):
  del params
  if used_out == {Usage.SCALAR_PREFETCH}:
    raise NotImplementedError('scalar prefetch not supported yet')
  elif used_out == {Usage.REGULAR}:
    return [
        {Usage.SCALAR_PREFETCH}
        if not ctx.avals_in[0].shape
        else {Usage.REGULAR}
    ]
  else:
    return [set()]

