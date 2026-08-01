
def _ndindexer_indices(
    indexer: indexing.NDIndexer, allow_arrays: bool = False
) -> tuple[Any, ...]:
  indices: list[Any] = []
  for idx in indexer.indices:
    if (isinstance(idx, mgpu.FragmentedArray) and idx.shape) or (
        isinstance(idx, ir.Value) and isinstance(idx.type, ir.VectorType)
    ):
      if not allow_arrays:
        raise ValueError("Arrays are not supported as indices.")
      indices.append(idx)
    elif not isinstance(idx, indexing.Slice):
      indices.append(_as_index(idx))
    elif not idx.is_dynamic_start and not idx.is_dynamic_size:
      indices.append(slice(idx.start, idx.start + idx.size, idx.stride))
    elif idx.stride == 1:
      if idx.is_dynamic_size:
        raise NotImplementedError("Dynamic slice size not supported.")
      indices.append(
          mgpu.DynamicSlice(
              _as_index(idx.start) if idx.is_dynamic_start else idx.start,  # pyrefly: ignore[bad-argument-type]
              int(idx.size),
          )
      )
    else:
      raise NotImplementedError(f"Unsupported slice: {idx}")
  return tuple(indices)

