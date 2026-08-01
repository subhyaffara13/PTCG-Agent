
def _squeeze_block_spec(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    dimensions: tuple[int, ...],
) -> Sequence[BlockIndexTransform]:
  del ctx
  if block_transform is no_block_index_transform:
    return [no_block_index_transform]

  def new_block_index_transform(*idxs):
    idx = block_transform.block_index_transform(*idxs)
    assert len(idx) == len(block_transform.block_shape)
    for dim in dimensions:
      idx = util.tuple_insert(idx, dim, 0)
    return idx

  new_block_shape = tuple(block_transform.block_shape)
  for dim in dimensions:
    new_block_shape = util.tuple_insert(new_block_shape, dim, None)

  return [block_transform.replace(
        block_shape=new_block_shape,
        block_index_transform=new_block_index_transform,
  )]

