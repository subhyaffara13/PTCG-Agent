
def _reduce_sum_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    axes: tuple[int, ...],
    out_sharding,
):
  del out_sharding
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  new_block_shape = []
  block_shape = iter(block_transform.block_shape)
  for i, d in enumerate(aval_in.shape):
    if i in axes:
      new_block_shape.append(pallas_core.Blocked(d))
    else:
      new_block_shape.append(next(block_shape))
  assert next(block_shape, None) is None

  def new_block_index_transform(*idxs):
    idx = block_transform.block_index_transform(*idxs)
    new_idx = []
    idx_iter = iter(idx)
    for i in range(len(aval_in.shape)):
      if i in axes:
        new_idx.append(0)
      else:
        new_idx.append(next(idx_iter))
    assert next(idx_iter, None) is None
    return tuple(new_idx)

  new_block_transform = block_transform.replace(
      block_shape=tuple(new_block_shape),
      block_index_transform=new_block_index_transform
  )
  return [new_block_transform]

