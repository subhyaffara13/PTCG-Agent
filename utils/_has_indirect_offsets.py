
def _has_indirect_offsets(
    transforms: Sequence[state.Transform],
    transforms_aval: Sequence[state.Transform],
    core_type: tpu_core.CoreType,
) -> bool:
  return any(
      _extract_indirect_offsets_from_indices(
          indexer.indices,
          indexer_aval.indices,  # pyrefly: ignore[missing-attribute]
          core_type,
          indexer.get_indexer_shape(),
      )
      is not None
      for indexer, indexer_aval in zip(transforms, transforms_aval)
      if isinstance(indexer, indexing.NDIndexer)
  )

