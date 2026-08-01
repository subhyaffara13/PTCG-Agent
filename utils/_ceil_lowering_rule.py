
def _ceil_lowering_rule(ctx: LoweringRuleContext, x):
  return mlir_math.ceil(x)

