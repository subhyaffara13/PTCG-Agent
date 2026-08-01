
def _multiple_of_wg_lowering_rule(ctx: LoweringRuleContext, val, *, values):
  [aval] = ctx.avals_in
  if aval.shape:
    raise NotImplementedError("multiple_of only supports scalar inputs.")
  for multiple in values:
    val = mgpu.dialect.assume_multiple(val, multiple)  # pyrefly: ignore[missing-attribute]
  return val

