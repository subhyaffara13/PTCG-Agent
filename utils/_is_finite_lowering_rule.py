
def _is_finite_lowering_rule(ctx: LoweringRuleContext, x):
  out_aval, = ctx.avals_out
  out_type = ctx.aval_to_ir_type(out_aval)
  return _not_lowering_rule(ctx, tpu.weird(out_type, x))

