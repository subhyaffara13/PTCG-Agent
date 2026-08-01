
def _population_count_lowering_rule(ctx: LoweringRuleContext, x):
  aval_out = ctx.avals_out[0]
  if not aval_out.shape:
    raise ValueError("Population count is not supported on scalars")
  return mlir_math.ctpop(x)

