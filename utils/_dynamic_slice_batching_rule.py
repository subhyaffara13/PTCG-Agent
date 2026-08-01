
def _dynamic_slice_batching_rule(batched_args, batch_dims, *, slice_sizes):
  # A dynamic slice is a special case of gather; we can delegate to the gather
  # batching rule.
  # TODO(phawkins): consider removing dynamic_slice entirely and using gather
  # always.
  # TODO(mattjj): Alternately, we could add jnp.unstack and an unstack_p,
  # since it should have easier rules (especially compared to gather).
  operand, *start_indices_and_dyn = batched_args
  operand_bd, *start_idx_and_dyn_bds = batch_dims
  ndims = operand.ndim - (0 if operand_bd is None else 1)
  dims = tuple(range(ndims))
  start_indices, dyn_slice_sizes = util.split_list(start_indices_and_dyn, [ndims])
  start_idx_bds, dyn_slice_size_bds = util.split_list(start_idx_and_dyn_bds, [ndims])
  dnums = GatherDimensionNumbers(
      offset_dims=dims,
      collapsed_slice_dims=(),
      start_index_map=dims,
  )
  index, index_bdim = _batch_dynamic_slice_indices(start_indices, start_idx_bds)
  return _gather_batching_rule(
    [operand, index, *dyn_slice_sizes],
    [operand_bd, index_bdim, *dyn_slice_size_bds], dimension_numbers=dnums,
    slice_sizes=slice_sizes, unique_indices=True, indices_are_sorted=True,
    mode=GatherScatterMode.CLIP, fill_value=None)

