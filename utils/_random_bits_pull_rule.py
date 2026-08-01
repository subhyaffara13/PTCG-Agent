
def _random_bits_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    **_,
):
  del ctx, block_transform
  key_block_transform = BlockIndexTransform(
      block_shape=None,
      memory_space=pallas_core.MemorySpace.KEY)
  return [key_block_transform]

