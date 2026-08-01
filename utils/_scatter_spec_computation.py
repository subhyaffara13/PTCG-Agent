
def _scatter_spec_computation(
    operand, indices, updates, dimension_numbers) -> P | None:
  """For a scatter, we consider the gather rules in inverse.

  We consider a gather, then convert to scatter as the inverse.
  A gather is a group of queries, each query slices a window out of `operand`.

  The `operand` dims sliced in to are those in `start_index_map`. Some of size 1
  dims in `start_index_map` are squeezed out of the gather output, termed
  `collapsed_slice_dims`. Hence `collapsed_slice_dims` is a subset of
  `start_index_map`. Confusingly, some of the slice sizes into `operand` can be
  full slices, hence it can be inferred that the corresponding start index of
  the window in that dim is 0 and hence the `operand` is not sliced in to.

  All dims of `indices`, except the final dim (`index_vector_dim`) are different
  queries in to `operand`. These queries may be batched with `operand`, and so
  are effectively N (query, operand) pairs so the queries are non-overlapping,
  each into different matching sized slices of `operand` (N being the batch
  dimension size), or unbatched where N queries are into the same `operand`. The
  actual indices of the start of the (fixed size) windows are contained in the
  final dimension of `indices`, the `index_vector_dim`.

  Some dims of `operand` are not sliced in to, these are `offset_dims`
  [offset_dims is defined from the gather output perspective (the `updates` in
  scatter) and by construction are the frontmost dims in `operand` after
  disregarding `collapsed_slice_dims` and `operand_batching_dims`].

  For a gather:
   - Batch dimensions must be resolvable unambiguously between `operand` and
   `indices`
   - Dims the `operand` is sliced in to are either full slices, or the `operand`
    is replicated in that dim (all the data for each query is present)
   - The `index_vector_dim` containing the actual start indices of the windows
   in to `operand` must be replicated

  A scatter is a group of queries, each of which has a corresponding window of
  `updates` to put in to `operand`.

  For a scatter:
   1 - Batch dimensions must resolve unambiguously between `operand`, `indices`
   and `updates`
   2 - Full slice dims must resolve unambiguously between `operand` and
   `updates`
   3 - Sub slice dims in `operand` and `updates` must be replicated.
   4 - `Indices` and `updates` must be replicated in dims where both are
   updating, possibly overlapping, subslices of operand. These are referred to
   as unbatched queries in the above description of gather.
   5 - The `index_vector_dim` containing the actual start indices of the windows
   in to `operand` must be replicated

  Not all dimensions updating slices in `operand` exist in `updates`. The
  `inserted_window_dims` provide size 1 updates into `operand` and are inserted
  into `updates`. We handle `operand` slices present in `updates`, then handle
  the inserted dims separately.

  Correspondance:
                Gather <-> Scatter
           offset_dims <-> update_window_dims
  collapsed_slice_dims <-> inserted_window_dims
       start_index_map <-> scatter_dims_to_operand_dims
  """
  operand_batching_dims = dimension_numbers.operand_batching_dims
  indices_batching_dims = dimension_numbers.scatter_indices_batching_dims
  update_window_dims = dimension_numbers.update_window_dims
  inserted_window_dims = dimension_numbers.inserted_window_dims
  index_vector_dim = indices.ndim - 1

  operand_spec = operand.sharding.spec
  indices_spec = indices.sharding.spec
  updates_spec = updates.sharding.spec

  if (all(s is None for s in operand_spec) and
      all(s is None for s in indices_spec) and
      all(s is None for s in updates_spec)):
    return P()

  updates_batching_dims = _get_updates_batching_dims(
      indices_batching_dims, update_window_dims, index_vector_dim, updates.shape)

  # Work out the corresponding operand dim for update window dims
  operand_window_dims = [
      i for i in range(operand.ndim)
      if i not in inserted_window_dims and i not in operand_batching_dims]

  # 1 - Batch dimensions must resolve unambiguously between `operand`, `indices`
  # and `updates`
  batch_dims_resolvable = all(
      _is_resolvable(operand_spec[od], indices_spec[id], updates_spec[ud])
      for od, id, ud in zip(
          operand_batching_dims, indices_batching_dims, updates_batching_dims))

  # 2 - Full slice dims must resolve unambiguously between `operand` and `updates`
  # 3 - Sub slice dims in `operand` and `updates` must be replicated.
  update_and_operand_window_dims_resolvable = all(
      (updates.shape[update_dim] == operand.shape[operand_dim] and
       updates_spec[update_dim] == operand_spec[operand_dim])
      or (updates_spec[update_dim] is None and operand_spec[operand_dim] is None)
      for update_dim, operand_dim in zip(
          update_window_dims, operand_window_dims))
  inserted_window_dims_replicated_in_operand = all(
      spec is None for i, spec in enumerate(operand_spec)
      if i in inserted_window_dims)

  # 4 - `Indices` and `updates` must be replicated in dims where both are
  # updating, possibly overlapping, slices of operand. These are referred to as
  # unbatched queries in the above description of gather.
  unbatched_query_dims_in_updates_replicated = all(
      spec is None for i, spec in enumerate(updates_spec)
      if i not in updates_batching_dims and i not in update_window_dims)
  unbatched_query_dims_in_indices_replicated = all(
      spec is None for i, spec in enumerate(indices_spec[:index_vector_dim])
      if i not in indices_batching_dims)

  # 5 - The `index_vector_dim` containing the actual start indices of the
  # windows in to `operand` must be replicated
  index_vector_dim_is_replicated = indices_spec[index_vector_dim] is None

  if (batch_dims_resolvable and
      update_and_operand_window_dims_resolvable and
      inserted_window_dims_replicated_in_operand and
      unbatched_query_dims_in_updates_replicated and
      unbatched_query_dims_in_indices_replicated and
      index_vector_dim_is_replicated):
    out_spec = list(operand_spec)

    # 1 - Batch dims
    for operand_dim, indices_dim, updates_dim in zip(
        operand_batching_dims, indices_batching_dims, updates_batching_dims):
      if out_spec[operand_dim] is None:
        out_spec[operand_dim] = (
            indices_spec[indices_dim] or updates_spec[updates_dim])
    # 2, 3 - Full/sub slices of operand dims present in updates
    for update_dim, operand_dim in zip(update_window_dims, operand_window_dims):
      if out_spec[operand_dim] is None:
        out_spec[operand_dim] = updates_spec[update_dim]
    return P(*out_spec)

  return None

