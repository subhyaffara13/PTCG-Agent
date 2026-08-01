
def _prng_random_bits_lowering_rule(ctx: LoweringRuleContext, *, shape):
  if len(shape) <= 1:
    # TODO(b/342054464): Support implicit dims for PRNGRandomBitsOp.
    raise NotImplementedError("random_bits only supports rank>=2 outputs.")
  out_aval = ctx.avals_out[0]
  out_type = ctx.aval_to_ir_type(out_aval)
  return tpu.prng_random_bits(out_type)

