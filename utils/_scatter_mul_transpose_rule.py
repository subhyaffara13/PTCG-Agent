
def _scatter_mul_transpose_rule(t, operand, indices, updates, *,
                                update_jaxpr, update_consts, dimension_numbers,
                                indices_are_sorted, unique_indices, mode):
  assert not ad.is_undefined_primal(indices)
  if ad.is_undefined_primal(updates):
    updates_shape = updates.aval.shape
  else:
    updates_shape = updates.shape
  if type(t) is ad_util.Zero:
    operand_t = ad_util.Zero(operand.aval) if ad.is_undefined_primal(operand) else None
    update_t = ad_util.Zero(updates.aval) if ad.is_undefined_primal(updates) else None
  else:
    operand_t = update_t = None
    if ad.is_undefined_primal(operand):
      operand_t = scatter_mul(
          t, indices, updates, dimension_numbers=dimension_numbers,
          indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
          mode=mode)
    if ad.is_undefined_primal(updates):
      if not unique_indices:
        raise NotImplementedError(
          "scatter_mul gradients are only implemented if `unique_indices=True`")
      gather_dnums = GatherDimensionNumbers(
          offset_dims=dimension_numbers.update_window_dims,
          collapsed_slice_dims=dimension_numbers.inserted_window_dims,
          start_index_map=dimension_numbers.scatter_dims_to_operand_dims,
          operand_batching_dims=dimension_numbers.operand_batching_dims,
          start_indices_batching_dims=dimension_numbers.scatter_indices_batching_dims,
      )
      slice_sizes = []
      pos = 0
      for i in range(len(t.shape)):
        if (
            i in dimension_numbers.inserted_window_dims
            or i in dimension_numbers.operand_batching_dims
        ):
          slice_sizes.append(1)
        else:
          slice_sizes.append(updates_shape[dimension_numbers.update_window_dims[pos]])
          pos += 1
      update_t = gather(lax.mul(t, operand), indices,
                        dimension_numbers=gather_dnums, slice_sizes=slice_sizes,
                        mode=mode, fill_value=0)
  return [operand_t, None, update_t]

