
def _is_trivial_indexer(indexer: indexing.NDIndexer):
  """Returns whether the indexer selects the entire shape."""
  for s, idx in zip(indexer.shape, indexer.indices):
    if not isinstance(idx, indexing.Slice):
      return False
    if idx.is_dynamic_start or idx.is_dynamic_size:
      return False
    if idx.start != 0 or idx.size != s:
      return False
  return True

