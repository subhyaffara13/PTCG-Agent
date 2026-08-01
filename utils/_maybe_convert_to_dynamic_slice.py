
def _maybe_convert_to_dynamic_slice(
    indexer: indexing.NDIndexer,
) -> (
    tuple[tuple[Array | int, ...], tuple[Array | int, ...], tuple[int, ...]]
    | None
):
  # An NDIndexer only corresponds to a `dynamic_slice` or `dynamic_update_slice`
  # if each of the indexers is a `Slice` or a ()-shaped value.
  if not all(isinstance(i, indexing.Slice) or not np.shape(i)
             for i in indexer.indices):
    return None

  # `lax.dynamic_slice` does not handle striding
  for i in indexer.indices:
    if isinstance(i, indexing.Slice) and i.stride > 1:
      return None

  _convert_i32 = lambda x: lax.convert_element_type(x, np.dtype("int32"))
  starts = tuple(
      _convert_i32(i.start) if isinstance(i, indexing.Slice)
      else _convert_i32(i) for i in indexer.indices
  )
  sizes = tuple(
      i.size if isinstance(i, indexing.Slice) else 1 for i in indexer.indices
  )
  squeeze_dims = tuple(
      i
      for i, idx in enumerate(indexer.indices)
      if not isinstance(idx, indexing.Slice)
  )
  return starts, sizes, squeeze_dims

