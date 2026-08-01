
def _is_contiguous_int4(block_info: BlockInfo, nd_indexer: NDIndexer) -> bool:
  """Returns True if the block is contiguous in the last dimension."""
  # In order to loaded as `uint8` the index must be an aligned slice.
  return (
      block_info.full_shape_dtype.dtype in (jnp.int4, jnp.uint4)
      and bool(block_info.start_indices_alignment)
      and (block_info.start_indices_alignment[-1] % 2 == 0)
      and isinstance(slc := nd_indexer.indices[-1], indexing.Slice)
      and isinstance(slc.start, int)
      and isinstance(slc.size, int)
      and (slc.start % 2 == 0)
      and (slc.size % 2 == 0)
      and (slc.stride == 1)
  )

