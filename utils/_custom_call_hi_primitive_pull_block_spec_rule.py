
def _custom_call_hi_primitive_pull_block_spec_rule(
    ctx: PullRuleContext, out_block_specs, *, _prim
):
  return _prim.pull_block_spec_rule(ctx, out_block_specs)

