
def _maybe_transpose_before_gather(
    indexer: indexing.NDIndexer
) -> tuple[int, ...] | None:
  is_int_indexing, _, _ = indexing.unpack_ndindexer(indexer)

  int_indexers_contiguous = bool(
      np.all(np.diff(np.where(is_int_indexing)[0]) == 1)
  )
  if int_indexers_contiguous:
    return None  # no transpose needed

  int_indexer_idxs: list[int] = []
  non_int_indexer_idxs: list[int] = []
  for i, is_int_index in enumerate(is_int_indexing):
    (int_indexer_idxs if is_int_index else non_int_indexer_idxs).append(i)
  transpose_order = (*int_indexer_idxs, *non_int_indexer_idxs)
  return transpose_order

