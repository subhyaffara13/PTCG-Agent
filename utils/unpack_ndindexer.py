
def unpack_ndindexer(indexer: NDIndexer) -> tuple[tuple[bool, ...],
                                                  tuple[Slice, ...],
                                                  tuple[IntIndexer, ...]]:
  # TODO(slebedev): Flip this to be ``is_slice_indexing`` and update callers.
  is_int_indexing = [not isinstance(i, Slice) for i in indexer.indices]
  slice_indexers, int_indexers = partition_list(
      is_int_indexing, indexer.indices)
  return tuple(is_int_indexing), tuple(slice_indexers), tuple(int_indexers)  # pyrefly: ignore [bad-return]

