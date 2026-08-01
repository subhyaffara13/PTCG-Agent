
def _erf_lowering_rule_wg(ctx: LoweringRuleContext, x):
  [x_aval] = ctx.avals_in
  return math_dialect.erf(_ensure_ir_value(x, x_aval.dtype))

