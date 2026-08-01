
def _atan2_lowering_rule(ctx: LoweringRuleContext, x, y, accuracy=None):
  if accuracy is not None:
    raise NotImplementedError("Not implemented: accuracy")

  x, y = _bcast(
      x,
      y,
      ctx.avals_in[0],
      ctx.avals_in[1],
      ctx.avals_out[0],
      ctx.lowering_context.dynamic_shape_replacement_fn,
  )
  return mlir_math.atan2(x, y)


def _atan2_lowering_rule(ctx: LoweringRuleContext, y, x):
  y, x = _bcast(y, x, *ctx.avals_in, *ctx.avals_out)
  return y.atan2(x)

