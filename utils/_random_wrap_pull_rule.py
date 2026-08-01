
def _random_wrap_pull_rule(
    ctx: PullRuleContext, block_transform: BlockIndexTransform, *, impl
):
  del ctx, block_transform, impl
  return [BlockIndexTransform(block_shape=None)]

