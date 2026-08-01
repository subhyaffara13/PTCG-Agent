
def _nextafter_lowering_rule(ctx: LoweringRuleContext, x, y):
  return lower_fun(
      pallas_utils.nextafter_lowering_helper,
  )(ctx, x, y)

