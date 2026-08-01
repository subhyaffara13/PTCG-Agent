
def _swap_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    **kwargs,
):
  del ctx, kwargs
  # The output and val block spec are the same.
  return [block_transform, block_transform]

