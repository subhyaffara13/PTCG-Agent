
def _reinterpret_int4_as_uint8(
    block_info: BlockInfo, nd_indexer: NDIndexer
) -> tuple[BlockInfo, NDIndexer]:
  """Returns a new block info and indexer that reads `int4` as `uint8`."""
  last_idx = nd_indexer.indices[-1]
  # pyrefly: ignore[missing-attribute]
  new_last_idx = indexing.Slice(last_idx.start // 2, last_idx.size // 2)
  new_indices = (*nd_indexer.indices[:-1], new_last_idx)
  new_shape = (*nd_indexer.shape[:-1], nd_indexer.shape[-1] // 2)
  idx = dataclasses.replace(nd_indexer, indices=new_indices, shape=new_shape)

  full_shape = block_info.full_shape_dtype.shape
  new_full_shape = (*full_shape[:-1], full_shape[-1] // 2)
  start_idx = block_info.start_indices[-1]
  new_start_idx = _floordiv(start_idx, _full(start_idx.type, 2), signed=False)
  new_start_indices = (*block_info.start_indices[:-1], new_start_idx)
  block_info = dataclasses.replace(
      block_info,
      full_shape_dtype=jax_core.ShapedArray(new_full_shape, jnp.uint8),
      start_indices=new_start_indices,
  )
  return block_info, idx

