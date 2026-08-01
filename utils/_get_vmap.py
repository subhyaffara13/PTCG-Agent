
def _get_vmap(batched_args, batched_dims, *, tree):
  axis_size, = {x.shape[d] for x, d in zip(batched_args, batched_dims)
                if d is not None}
  ref, *flat_idxs = batched_args
  ref_dim, *flat_idx_dims = batched_dims
  indexers = tree_util.tree_unflatten(tree, flat_idxs)
  if not indexers:
    return get_p.bind(ref, *flat_idxs, tree=tree), ref_dim
  indexers_dims = tree_util.tree_unflatten(tree, flat_idx_dims)

  idx_is_batched = any(i_dim is not None
                       for i_dim in flat_idx_dims)
  if len(indexers) > 1:
    raise NotImplementedError("Batching with multiple indexers not supported.")

  # TODO(sharadmv): handle vmap of multiple indexers
  new_indexers = tuple(_batch_indexer(indexer, dims, axis_size,
                                  ref.shape, ref_dim, idx_is_batched)
                     for indexer, dims in zip(indexers, indexers_dims))
  flat_indexers, tree = tree_util.tree_flatten(new_indexers)

  is_int_indexing, _, _ = indexing.unpack_ndindexer(indexers[0])
  int_indexers_contiguous = bool(
      np.all(np.diff(np.where(is_int_indexing)[0]) == 1)
  )
  # Note: _batch_indexer will add a slice for the batch dim if the int_indexer
  # shape is empty, else it will use advanced/int indexing.
  will_add_int_batcher = ref_dim is not None and (idx_is_batched or indexers[0].int_indexer_shape)

  is_new_int_indexing, _, _ = indexing.unpack_ndindexer(new_indexers[0])
  new_int_indexers_contiguous = bool(
      np.all(np.diff(np.where(is_new_int_indexing)[0]) == 1)
  )

  out = get_p.bind(ref, *flat_indexers, tree=tree)
  should_transpose = (int_indexers_contiguous and
                      not new_int_indexers_contiguous)
  if will_add_int_batcher and should_transpose:
    original_pos = is_int_indexing.index(True)
    array_indexer_shape = new_indexers[0].int_indexer_shape
    array_indexer_len = len(array_indexer_shape)

    transpose_order = list(range(len(out.shape)))
    transpose_order = (
        transpose_order[0],
        *transpose_order[array_indexer_len:array_indexer_len+original_pos],
        *transpose_order[1:array_indexer_len],
        *transpose_order[array_indexer_len+original_pos:],
    )
    out = lax.transpose(out, transpose_order)
    out_bdim = 0
  else:
    if ref_dim is not None:
      if will_add_int_batcher:
        if not int_indexers_contiguous:
          # In this case the indexer is always moved to the front.
          out_bdim = 0
        else:
          # In this case the indexer is not moved to the front.
          out_bdim = is_new_int_indexing.index(True)
      else:
        # We only trigger this case when the int_indexer shape is empty,
        # so we don't need to account for int_indexer_shape.
        int_indexers_before_ref_dim = sum(is_new_int_indexing[:ref_dim])
        out_bdim = ref_dim - int_indexers_before_ref_dim
    else:
      out_bdim = 0
      if new_int_indexers_contiguous:
        out_bdim = is_new_int_indexing.index(True)
  return out, out_bdim

