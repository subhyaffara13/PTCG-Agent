
def _is_dynamic(indexer: indexing.NDIndexer) -> bool:
  return any(
      isinstance(idx, indexing.Slice)
      and (idx.is_dynamic_start or idx.is_dynamic_size)
      for idx in indexer.indices
  )

