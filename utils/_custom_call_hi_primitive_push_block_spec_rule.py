
def _custom_call_hi_primitive_push_block_spec_rule(
    ctx: PullRuleContext, *block_specs, _prim
):
  return _prim.push_block_spec_rule(ctx, block_specs)

