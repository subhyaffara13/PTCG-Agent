
def _extract_indirect_offsets(
    transforms: Sequence[state.Transform],
    expected_shape: tuple[int, ...],
    transforms_aval: Sequence[state.Transform],
    core_type: tpu_core.CoreType,
) -> tuple[sc_core.Indices | None, Sequence[state.Transform]]:
  for i, (indexer, indexer_aval) in enumerate(zip(transforms, transforms_aval)):
    if not isinstance(indexer, indexing.NDIndexer):
      continue
    assert isinstance(indexer_aval, indexing.NDIndexer)
    offsets = _extract_indirect_offsets_from_indices(
        indexer.indices,
        indexer_aval.indices,
        core_type,
        indexer.get_indexer_shape(),
        expected_shape,
    )
    if offsets is None:
      continue
    # The slices applied to other dimensions are processed independently of
    # indirect offsets.
    split_indices = (indexing.Slice(0, indexer.shape[0]), *indexer.indices[1:])
    split_indexer = indexing.NDIndexer(split_indices, indexer.shape, ())
    if i != len(transforms) - 1:
      raise NotImplementedError(
          "The indexed ref in scatter/gather via `pltpu.async_copy` cannot have"
          " any transforms following the indexer"
      )
    return offsets, [*transforms[:i], split_indexer]

  return None, transforms

