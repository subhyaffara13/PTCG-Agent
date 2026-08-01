
def _broadcast_in_dim_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    shape: tuple[int, ...],
    broadcast_dimensions: tuple[int, ...],
    sharding: jax.sharding.Sharding,
):
  del shape, sharding

  shape = ctx.avals_in[0].shape
  if not shape:
    return [no_block_index_transform]

  def new_block_index_transform(*idxs):
    idx = block_transform.block_index_transform(*idxs)
    return tuple(
        0 if (d == 1) else idx[i]
        for i, d in zip(broadcast_dimensions, shape, strict=True)
    )

  new_block_shape = tuple(
      b if ((b := block_transform.block_shape[i]) is None) or (d != 1) else 1
      for i, d in zip(broadcast_dimensions, shape, strict=True)
  )
  return [block_transform.replace(
      block_shape=new_block_shape,
      block_index_transform=new_block_index_transform)]

