
def _unary_warp_lowering_rule(impl):
  def _lowering_rule(ctx: LoweringRuleContext, x):
    if not all(aval_in.shape == () for aval_in in ctx.avals_in):
      raise NotImplementedError(
          "Non-scalar arithmetic is not supported in warp-level lowering.")
    return impl(x)
  return _lowering_rule

