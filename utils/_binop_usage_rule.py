
def _binop_usage_rule(prim, ctx, used_out: set[Usage], **params):
  del prim
  del params  # unused
  if used_out == {Usage.SCALAR_PREFETCH}:
    return [{Usage.SCALAR_PREFETCH}, {Usage.SCALAR_PREFETCH}]
  elif used_out == {Usage.REGULAR}:
    usage = [{Usage.REGULAR} for _ in ctx.avals_in]
    return usage
  else:
    return [set()] * len(ctx.avals_in)

