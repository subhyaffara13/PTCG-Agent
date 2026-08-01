
def _atan2_lowering_rule_wg(ctx: LoweringRuleContext, y, x):
  y, x = _bcast_wg(y, x, *ctx.avals_in, *ctx.avals_out)
  return math_dialect.atan2(y, x)

