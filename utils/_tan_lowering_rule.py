
def _tan_lowering_rule(ctx: LoweringRuleContext, x, accuracy=None):
  if accuracy is not None:
    raise NotImplementedError("Not implemented: accuracy")
  return mlir_math.tan(x)

