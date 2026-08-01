
def _batch_indexer(
    indexer: indexing.NDIndexer,
    dims,
    axis_size: int,
    ref_shape: tuple[int, ...],
    ref_dim: int | batching.NotMapped,
    idx_is_batched: bool,
) -> indexing.NDIndexer:
  """Converts a batched indexer into an unbatched one.

  This function handles the complexity of `vmap`-style batching where either the
  `ref` being indexed, the indexer, or both may have batched dimensions. The
  goal is to produce a new indexer that acts as if applied in a batched context,
  but without actual batching, enabling downstream code to process it as usual.

  If any index in `indexer` is batched, all array indexers are normalized. If
  the array indexer contains a batched dimension, the dimension is moved to the
  front (axis 0). If the array indexer not batched, it is broadcasted to include
  a batch dimension at the front. This is to guarantee that all array indexers
  are still of the same shape.

  Slices are passed through unchanged unless they contain dynamic elements and
  are themselves batched, which is currently unsupported.

  If `ref` is batched (`ref_dim` is not `NotMapped`), we simulate per-example
  indexing by inserting a new iota array at the position corresponding to
  `ref_dim` in the indexer.

  It is worth noting that if the array indexers in the original indexer are
  contiguous, but become non-contiguous in the new indexer due to the insertion
  of the iota, the dimensions corresponding to the array indexers will be moved
  to the front in the indexing result. The batched dimension will be at axis 0,
  while the dimensions corresponding to the array indexers in the original
  indexer will start from axis 1. This behavior would cause a mismatch between
  the original indexer and the new indexer. Callers must take this behavior into
  account and properly transpose the arrays involved to avoid this mismatch.

  Args:
    indexer: An `NDIndexer` that indexes into `ref`.
    dims: A pytree with the same structure as `indexer`, indicating which
      dimension (if any) is batched for each array indexer.
    axis_size: Size of the batch dimension.
    ref_shape: Shape of `ref`.
    ref_dim: The dimension of `ref` that is batched (if any).
    idx_is_batched: Whether any index in the `indexer` is batched.
  """
  indices = indexer.indices
  indices_dims = dims.indices
  new_indices: list[Array | indexing.Slice | int] = []
  new_integer_indexer_shape = (axis_size, *indexer.int_indexer_shape)
  for idx, dim in zip(indices, indices_dims):
    if idx_is_batched:
      # If at least one of the idx is batched, we broadcast them all and move the
      # batch dim to the front.
      if isinstance(idx, indexing.Slice):
        # size is static, but start can be dynamic
        # Check if start is static (which it can be)
        is_static_slice = len(tree_util.tree_leaves(idx)) == 0
        if is_static_slice:
          new_indices.append(idx)
          continue
        dim = dim.start
        if dim is None:
          # Broadcasting the slice is free (the start index stays the same)
          new_indices.append(idx)
        else:
          raise NotImplementedError(
              f"No support for vmapping over nontrivial slices just yet: {idx}")
      else:
        # Check if we are indexing with a scalar or not. If we are indexing
        # with a scalar and we are not batched, we can avoid broadcasting it.
        if not shapeof(idx):
          new_indices.append(idx)
        else:
          if dim is None:
            bcast_dims = tuple(range(1, np.ndim(idx) + 1))
            idx = lax.broadcast_in_dim(idx, new_integer_indexer_shape,
                                       bcast_dims)
          else:
            idx = batching.moveaxis(idx, dim, 0)
          new_indices.append(idx)
    else:
      if ref_dim is not None:
        if not isinstance(idx, indexing.Slice):
          if shapeof(idx):
            bcast_dims = tuple(range(1, core.typeof(idx).ndim + 1))
            idx = lax.broadcast_in_dim(idx, new_integer_indexer_shape,
                                       bcast_dims)
      new_indices.append(idx)

  # if the ref is batched, we must insert an indexer for that new axis
  if ref_dim is not None:
    # sometimes can optimize to generate a slice(None) on the batch axis.
    # NOTE this optimization has caused much pain. if in doubt, try removing.
    if not idx_is_batched and not indexer.int_indexer_shape:
      batch_idx = indexing.Slice(0, axis_size)
      new_integer_indexer_shape = ()
    else:
      batch_idx = lax.broadcasted_iota(
          np.dtype('int32'), new_integer_indexer_shape, 0)
    new_indices.insert(ref_dim, batch_idx)

  return indexing.NDIndexer(
      tuple(new_indices), ref_shape, new_integer_indexer_shape, validate=True
  )

