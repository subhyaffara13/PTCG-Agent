
def _compute_pointers_from_indices(
    root_ptr: ir.Value, block_info: BlockInfo, nd_indexer: NDIndexer
) -> ir.Value:
  offsets = _compute_offsets_from_indices(block_info, nd_indexer)
  shape = nd_indexer.get_indexer_shape_static()
  return _add(_bcast_to(root_ptr, shape), offsets)

