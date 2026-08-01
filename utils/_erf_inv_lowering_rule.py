
def _erf_inv_lowering_rule(ctx: LoweringRuleContext, x):
  return lower_fun(
      pallas_utils.erf_inv_lowering_helper,
  )(ctx, x)

