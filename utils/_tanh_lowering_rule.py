
def _tanh_lowering_rule(ctx: LoweringRuleContext, x, accuracy=None):
  if accuracy is not None:
    raise NotImplementedError("Not implemented: accuracy")
  return mlir_math.tanh(x)


def _tanh_lowering_rule(ctx: LoweringRuleContext, x, accuracy):
  if accuracy is not None:
    raise NotImplementedError("Not implemented: accuracy")
  [x_aval] = ctx.avals_in
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    return _ensure_fa(x, x_aval.dtype).tanh(approx=ctx.module_ctx.approx_math)
  fastmath = (
      arith_dialect.FastMathFlags.afn if ctx.module_ctx.approx_math else None
  )
  return math_dialect.tanh(_ensure_ir_value(x, x_aval.dtype), fastmath=fastmath)

