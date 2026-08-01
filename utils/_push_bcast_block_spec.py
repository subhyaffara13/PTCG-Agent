
def _push_bcast_block_spec(
    block_spec: pallas_core.BlockSpec,
    i: int,
    size: int,
) -> pallas_core.BlockSpec:

  bcast_dim_block_shape = size
  if isinstance(block_spec.block_shape[i], pallas_core.Element):
    bcast_dim_block_shape = pallas_core.Element(size)
  new_block_shape = util.tuple_update(
      block_spec.block_shape, i, bcast_dim_block_shape
  )
  return pallas_core.BlockSpec(new_block_shape, block_spec.index_map)

