
def _eltwise_pull_rule(
    prim: core.Primitive,
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    **params,
) -> Sequence[BlockIndexTransform]:
  del prim, ctx, params
  return [block_transform]

