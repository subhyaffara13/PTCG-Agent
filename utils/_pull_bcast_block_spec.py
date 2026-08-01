
def _pull_bcast_block_spec(
    block_transform: BlockIndexTransform, i: int
) -> BlockIndexTransform:
  def new_block_index_transform(*idxs):
    idx = block_transform.block_index_transform(*idxs)
    assert len(idx) == len(block_transform.block_shape)
    idx = util.tuple_update(idx, i, 0)
    return idx

  if block_transform.block_shape[i] is None:
    return block_transform.replace(
        block_index_transform=new_block_index_transform)

  # TODO(wdvi): This is a hack needed since lowering rules require block shape
  # to contain either all pl.Element or none
  bcast_dim_block_shape = 1
  if isinstance(block_transform.block_shape[i], pallas_core.Element):
    bcast_dim_block_shape = pallas_core.Element(1)
  new_block_shape = util.tuple_update(
      block_transform.block_shape, i, bcast_dim_block_shape
  )
  return block_transform.replace(
      block_shape=new_block_shape,
      block_index_transform=new_block_index_transform,
  )

