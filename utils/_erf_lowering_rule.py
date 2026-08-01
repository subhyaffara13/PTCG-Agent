
def _erf_lowering_rule(ctx: LoweringRuleContext, x, accuracy=None):
  if accuracy is not None:
    raise NotImplementedError("Not implemented: accuracy")
  return mlir_math.erf(x)


def _erf_lowering_rule(ctx: LoweringRuleContext, x):
  [x_aval] = ctx.avals_in
  return _ensure_fa(x, x_aval.dtype).erf()

