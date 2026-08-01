
def _transpose_lowering_rule(ctx: LoweringRuleContext, x, *, permutation):
  out_type = ctx.aval_to_ir_type(ctx.avals_out[0])
  return tpu.transpose(out_type, x, permutation)

