
def _addupdate_vmap(axis_data, batched_args, batched_dims, *, tree):
  ref, val, *flat_idxs = batched_args
  ref_dim, val_dim, *flat_idx_dims = batched_dims
  indexers = tree_util.tree_unflatten(tree, flat_idxs)
  indexers_dims = tree_util.tree_unflatten(tree, flat_idx_dims)

  ref_is_batched = ref_dim is not None
  val_is_batched = val_dim is not None
  idx_is_batched = any(i_dim is not None
                       for i_dim in flat_idx_dims)

  if not ref_is_batched:
    raise Exception("performing an addupdate operation with vmapped value on "
                    f"an unbatched array reference of type {core.typeof(ref)}. "
                    "Move the array reference to be an argument to the vmapped "
                    "function?")
  if not indexers:
    if val_dim != ref_dim:
      val = batching.matchaxis(axis_data, val_dim, ref_dim, val)
    return addupdate_p.bind(ref, val, *flat_idxs, tree=tree), []
  if len(indexers) > 1:
    raise NotImplementedError("Batching with multiple indexers not supported.")

  # TODO(sharadmv): handle vmap of multiple indexers
  new_indexers = tuple(_batch_indexer(indexer, dims, axis_data.size,
                                      ref.shape, ref_dim, idx_is_batched)
                       for indexer, dims in zip(indexers, indexers_dims))
  flat_indexers, tree = tree_util.tree_flatten(new_indexers)

  is_int_indexing, _, _ = indexing.unpack_ndindexer(indexers[0])
  int_indexers_contiguous = bool(
      np.all(np.diff(np.where(is_int_indexing)[0]) == 1)
  )
  is_new_int_indexing, _, _ = indexing.unpack_ndindexer(new_indexers[0])
  new_int_indexers_contiguous = bool(
      np.all(np.diff(np.where(is_new_int_indexing)[0]) == 1)
  )

  # Note: _batch_indexer will add a slice for the batch dim if the int_indexer
  # shape is empty, else it will use advanced/int indexing.
  will_add_int_batcher = idx_is_batched or indexers[0].int_indexer_shape

  if not new_int_indexers_contiguous and will_add_int_batcher:
    batched_dim_in_result = 0  # will be moved to the front
  elif any(is_new_int_indexing):
    if will_add_int_batcher:
      # _batch_indexer ensures the bdim in the int indexers is at the front
      batched_dim_in_result = is_new_int_indexing.index(True)
    else:
      # all int indices are scalars, so the ones before ref_dim disappear
      assert ref_dim is not None
      batched_dim_in_result = ref_dim - sum(is_new_int_indexing[:ref_dim])
  else:
    batched_dim_in_result = ref_dim

  if not val_is_batched:
    if ref_is_batched or idx_is_batched:
      val = batching.broadcast(val, axis_data.size, batched_dim_in_result,
                               axis_data.explicit_mesh_axis)
  else:
    assert batched_dim_in_result is not None
    val = batching.moveaxis(val, val_dim, batched_dim_in_result)

  # Originally not going to be moved to the front, but now going to be moved to
  # the front.
  if int_indexers_contiguous and not new_int_indexers_contiguous and will_add_int_batcher:
    original_pos = is_int_indexing.index(True)
    array_indexer_shape = new_indexers[0].int_indexer_shape
    array_indexer_len = len(array_indexer_shape)

    transpose_order = list(range(len(val.shape)))
    transpose_order = (
        transpose_order[0],
        *transpose_order[1+original_pos:(1+original_pos)+(array_indexer_len-1)],
        *transpose_order[1:1+original_pos],
        *transpose_order[(1+original_pos)+(array_indexer_len-1):],
    )
    val = val.transpose(transpose_order)

  return addupdate_p.bind(ref, val, *flat_indexers, tree=tree), []

