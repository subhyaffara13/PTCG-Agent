
def _gather_spec_computation(operand, indices, dimension_numbers, slice_sizes):
  """Returns gather output sharding spec if unambiguous, else None.

  Operand dimensions can be split into:
    1. Batching dims which must resolve unambiguously with the corresponding
      indices batching dims. `operand_batching_dims` in GatherDimensionNumbers.
    2. Sliced dims which must be replicated. These are the subset of dims in
      `start_index_map` where the slice size is not equal to the operand size.
      A further subset of these (`collapsed_slice_dims`) are collapsed in the
      output.
    3. Unsliced dims, these correspond directly to dimensions in the
      output and so propagate their shardings. These are the dimensions not
      batched or sliced.

  Indices dimensions can be split into:
    1. Batching dims which must resolve unambiguously with the corresponding
      operand batching dims. `start_indices_batching_dims` in
      GatherDimensionNumbers.
    2. Index vector dim which contains the start indices for each dimension of
      the operand sliced in to. This must be replicated. It is the last
      dimension of indices.
    3. Other dims which correspond directly to dimensions in the output and
      so propagate their shardings. These are the dimensions not present in
      index batching dims and index vector dim.

  If the axes of the corresponding batching dims between operand and indices are
  both not None and do not match, then sharding propagation cannot be resolved
  unambiguously and so we return None.
  """
  offset_dims = dimension_numbers.offset_dims
  start_index_map = dimension_numbers.start_index_map
  collapsed_slice_dims = dimension_numbers.collapsed_slice_dims
  operand_batching_dims = dimension_numbers.operand_batching_dims
  start_indices_batching_dims = dimension_numbers.start_indices_batching_dims
  output_shape_rank = len(offset_dims) + indices.ndim - 1

  operand_spec = operand.sharding.spec
  indices_spec = list(indices.sharding.spec)

  if (all(s is None for s in operand_spec) and
      all(s is None for s in indices_spec)):
    return P()

  assert all(i in start_index_map for i in collapsed_slice_dims)

  # start_index_map defined which operand dimensions are sliced in to. However,
  # if that slice is a full slice then we can propagate the sharding.
  operand_index_dims_full_slice_or_replicated = all(
      slice_sizes[i] == operand.shape[i] or operand_spec[i] is None
      for i in start_index_map)
  batching_dims_resolve_unambiguously = all(
      indices_spec[indices_dim] == operand_spec[operand_dim]
      or operand_spec[operand_dim] is None
      or indices_spec[indices_dim] is None
      for (operand_dim, indices_dim) in zip(
          operand_batching_dims, start_indices_batching_dims)
  )
  # Leads to comms on the bwd pass in scatter
  indices_non_batch_dims_replicated = all(
      s is None for i, s in enumerate(indices_spec)
      if i not in start_indices_batching_dims
  )

  if (operand_index_dims_full_slice_or_replicated
      and batching_dims_resolve_unambiguously
      and indices_non_batch_dims_replicated):
    # Resolve any batched shardings into indices shardings.
    for operand_dim, indices_dim in zip(
        operand_batching_dims, start_indices_batching_dims):
      assert (indices_spec[indices_dim] == operand_spec[operand_dim]
              or indices_spec[indices_dim] is None
              or operand_spec[operand_dim] is None)
      # Resolution and propagation of batching_dims is handled in indices,
      # operand_batching_dims spec is resolved into indices spec (to match how
      # the gather shape rule resolves output dimensions).
      indices_spec[indices_dim] = indices_spec[indices_dim] or operand_spec[operand_dim]

    slice_sizes_gen = (
        (i, s) for i, s in enumerate(slice_sizes)
        if i not in collapsed_slice_dims and i not in operand_batching_dims)
    indices_spec_gen = iter(indices_spec)

    out_spec = []
    for i in range(output_shape_rank):
      if i in offset_dims:
        # The offset dims are the set of dimensions in the `gather` output that
        # derive solely from the operand.
        operand_dim, slice_size = next(slice_sizes_gen)
        # Due to the `operand_index_dims_full_slice_or_replicated` check, if a
        # slice is not full, it must be replicated.
        assert (slice_size == operand.shape[operand_dim]
                or operand_spec[operand_dim] is None)
        out_spec.append(operand_spec[operand_dim])
      else:
        # The other dimensions are either batching dims (which derive from both
        # indices and operand, and we resolved above) or solely from indices.
        out_spec.append(next(indices_spec_gen))
    return P(*out_spec)
  return None

