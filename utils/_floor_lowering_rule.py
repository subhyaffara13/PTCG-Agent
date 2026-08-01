
def _floor_lowering_rule(ctx: LoweringRuleContext, x):
  return mlir_math.floor(x)

