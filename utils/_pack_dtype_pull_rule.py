
def _pack_dtype_pull_rule(
    ctx: block_spec.PullRuleContext,
    block_spec: pallas_core.BlockSpec,
    *,
    dtype: FusionDType,
):
  aval_out = ctx.avals_out[0]
  return dtype.pull_block_spec_one_step(aval_out, block_spec)

