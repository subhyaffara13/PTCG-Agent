
def merge_indexers(
    indexers: Sequence[indexing.NDIndexer]) -> indexing.NDIndexer:
  """Merges multiple indexers into a single indexer.

  This function computes a new indexer such that applying the
  new indexer produces the same result as applying the sequence
  of input indexers in order from first-to-last.
  """
  if len(indexers) == 0:
    raise ValueError("Cannot merge empty list of indexers")
  if len(indexers) == 1:
    return indexers[0]
  root_shape = indexers[0].shape
  current_indices = [indexing.Slice(0, size, 1) for size in root_shape]
  removed_dimensions = set()
  for indexer in indexers:
    if indexer.int_indexer_shape:
      raise NotImplementedError()

    def _ensure_idx_fa(x: Any) -> mgpu.FragmentedArray:
      i32 = ir.IntegerType.get_signless(32)
      if isinstance(x, ir.Value):
        # TODO(cperivol): We assume all indices are signed. We should
        # look at the JAX avals to see if the integers are signed or
        # not to figure out is_signed.
        is_signed = False if isinstance(x.type, ir.IntegerType) else None
        return mgpu.FragmentedArray.splat(x, (), is_signed=is_signed).astype(
            i32, is_signed=False
        )
      if isinstance(x, mgpu.FragmentedArray):
        return x.astype(i32, is_signed=False)
      if isinstance(x, int):
        return mgpu.FragmentedArray.splat(mgpu.c(x, i32), (), is_signed=False)
      if (
          isinstance(x, jax_literals.TypedNdArray)
          and x.ndim == 0
          and np.issubdtype(x.dtype, np.signedinteger)
      ):
        return mgpu.FragmentedArray.splat(
            mgpu.c(int(x), i32), (), is_signed=False
        )
      raise NotImplementedError(x)

    num_skipped = 0
    for i in range(len(current_indices)):
      # Integer indexers remove dimensions which should be
      # skipped by following indexers.
      if i in removed_dimensions:
        num_skipped += 1
        continue
      dim_indexer = indexer.indices[i - num_skipped]
      current_index = current_indices[i]
      assert isinstance(current_index, indexing.Slice)

      current_start_index = _ensure_idx_fa(current_index.start)
      if isinstance(dim_indexer, indexing.Slice):
        if dim_indexer.stride != 1:
          raise NotImplementedError("Non-unit strides not implemented.")
        current_indices[i] = indexing.Slice(
            current_start_index + _ensure_idx_fa(dim_indexer.start),
            dim_indexer.size,
            1,
        )
      else:
        current_indices[i] = current_start_index + _ensure_idx_fa(dim_indexer)
        removed_dimensions.add(i)
  return indexing.NDIndexer(
      indices=tuple(current_indices),
      shape=root_shape,
      int_indexer_shape=(),
  )

