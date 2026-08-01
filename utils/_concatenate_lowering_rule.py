
def _concatenate_lowering_rule(ctx: LoweringRuleContext, *xs, dimension):
  del ctx  # Unused.
  return tpu.concatenate(xs, dimension=dimension)


def _concatenate_lowering_rule(ctx: LoweringRuleContext, *args, dimension):
  if len(args) != 2:
    raise NotImplementedError("Only 2-argument concatenate is supported.")
  x_aval, y_aval = ctx.avals_in
  x, y = args
  if dimension != x_aval.ndim-1:
    raise NotImplementedError(
        "Only concatenate along the last dimension is supported."
    )
  if x_aval.shape[-1] != 1 or y_aval.shape[-1] != 1:
    raise NotImplementedError(
        "Only arguments with shape [..., 1] are supported."
    )
  lhs = _reshape(x, x_aval.shape[:-1])
  rhs = _reshape(y, y_aval.shape[:-1])
  ret_type = get_join_type(ir.RankedTensorType(rhs.type))
  return tt_dialect.join(ret_type, lhs, rhs)

