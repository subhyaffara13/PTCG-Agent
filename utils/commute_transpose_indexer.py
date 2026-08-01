
def commute_transpose_indexer(
    _: jax_core.AbstractValue,
    transpose: state_types.TransposeTransform,
    indexer: indexing.NDIndexer,
) -> tuple[indexing.NDIndexer, state_types.TransposeTransform]:
  idxs = indexer.indices
  removed_dims = [
      i
      for i, idx in enumerate(idxs)
      if not isinstance(idx, (slice, indexing.Slice))
  ]
  new_perm = tuple(
      p - sum(d < p for d in removed_dims)
      for p in transpose.permutation
      if p not in removed_dims
  )
  new_shape = tuple(
      indexer.shape[i] for i in state_types._perm_inverse(transpose.permutation)
  )
  new_idxs = tuple(
      idxs[i] for i in state_types._perm_inverse(transpose.permutation)
  )
  new_indexer = indexing.NDIndexer.from_indices_shape(
      indices=new_idxs, shape=new_shape
  )
  return new_indexer, state_types.TransposeTransform(new_perm)

