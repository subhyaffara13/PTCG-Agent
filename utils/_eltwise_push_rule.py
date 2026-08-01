
def _eltwise_push_rule(
    prim: core.Primitive,
    ctx: PullRuleContext,
    block_spec: pallas_core.BlockSpec,
    **params,
) -> pallas_core.BlockSpec:
  del prim, ctx, params
  return block_spec

