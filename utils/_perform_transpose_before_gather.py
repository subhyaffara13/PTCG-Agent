
def _perform_transpose_before_gather(
    target_arr: Array,
    indexer: indexing.NDIndexer,
    transpose_order: tuple[int, ...],
) -> tuple[Array, indexing.NDIndexer]:
  new_target_arr = target_arr.transpose(transpose_order)
  reordered_indices = tuple(indexer.indices[i] for i in transpose_order)
  new_indexer = indexing.NDIndexer(
      indices=reordered_indices,
      shape=indexer.shape,
      int_indexer_shape=indexer.int_indexer_shape,
  )
  return new_target_arr, new_indexer

