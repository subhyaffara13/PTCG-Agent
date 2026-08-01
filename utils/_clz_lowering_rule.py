
def _clz_lowering_rule(ctx: LoweringRuleContext, x):
  return mlir_math.ctlz(x)


def _clz_lowering_rule(ctx: LoweringRuleContext, x):
  [x_aval] = ctx.avals_in
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    return _ensure_fa(x, x_aval.dtype)._pointwise(math_dialect.ctlz, restrict_bitwidth=False)
  x = _ensure_ir_value(x, x_aval.dtype)
  return math_dialect.ctlz(x)

