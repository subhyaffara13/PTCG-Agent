
def _copysign_lowering_rule(ctx: LoweringRuleContext, x1, x2):
  [x1_aval, x2_aval] = ctx.avals_in
  x1 = _ensure_fa(x1, x1_aval.dtype)
  x2 = _ensure_fa(x2, x2_aval.dtype)
  return x1.copysign(x2)


def _copysign_lowering_rule(ctx: LoweringRuleContext, x1, x2):
  [x1_aval, x2_aval] = ctx.avals_in
  x1 = _ensure_ir_value(x1, x1_aval.dtype)
  x2 = _ensure_ir_value(x2, x2_aval.dtype)
  return math_dialect.copysign(x1, x2)

