from typing import Any

def _convert_to_gather_arrays(indexer: indexing.NDIndexer) -> tuple[Array, ...]:
  # This is the general gather case. We need to create the gather arrays.
  total_shape = indexer.get_indexer_shape()
  is_int_indexing, _, _ = indexing.unpack_ndindexer(indexer)

  if any(is_int_indexing):
    n_idxers = len(indexer.indices)
    int_indexer_shape = indexer.int_indexer_shape
    n_int_indexers = sum(1 for p in is_int_indexing if p)
    last_int_index_idx = n_idxers - 1 - is_int_indexing[::-1].index(True)
    n_slice_index_dims_after_int = n_idxers - last_int_index_idx - 1
  else:
    n_idxers = 0
    last_int_index_idx = 0

  def get_idx_in_shape_after_indexing(i):
    if not any(is_int_indexing):
      return i

    if i < n_idxers - n_slice_index_dims_after_int - n_int_indexers:
      return i
    if i < n_idxers - n_slice_index_dims_after_int:
      raise ValueError
    return i - n_int_indexers + len(int_indexer_shape)

  arrs: list[Any] = []
  for i, idxer in enumerate(indexer.indices):
    if isinstance(idxer, indexing.Slice):
      idx_in_shape_after_indexing = get_idx_in_shape_after_indexing(i)
      arr = (
          lax.iota(np.int32, total_shape[idx_in_shape_after_indexing])
          * idxer.stride
          + idxer.start
      )
      diff = len(total_shape) - idx_in_shape_after_indexing - 1
      arr = arr.reshape(arr.shape + (1,) * diff)
      arrs.append(arr)
    elif isinstance(idxer, (np.ndarray, Array)):
      diff = n_idxers - 1 - last_int_index_idx
      arr = idxer.reshape(idxer.shape + (1,) * diff)
      arrs.append(arr)
    else:
      raise ValueError(f"Invalid type of idxer: {type(idxer).__name__}")

  return tuple(arrs)

