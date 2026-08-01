
def _gather_transpose_rule(t, operand, indices, *, dimension_numbers,
                           slice_sizes, unique_indices, indices_are_sorted,
                           mode, fill_value):
  assert ad.is_undefined_primal(operand)
  if type(t) is ad_util.Zero:
    out = ad_util.Zero(operand.aval)
  else:
    zeros = lax.full(operand.aval.shape, 0, typeof(t).dtype,
                     sharding=operand.aval.sharding)
    zeros = core.pvary(zeros, tuple(operand.aval.mat.varying))
    scatter_dnums = ScatterDimensionNumbers(
        update_window_dims=dimension_numbers.offset_dims,
        inserted_window_dims=dimension_numbers.collapsed_slice_dims,
        scatter_dims_to_operand_dims=dimension_numbers.start_index_map,
        operand_batching_dims=dimension_numbers.operand_batching_dims,
        scatter_indices_batching_dims=dimension_numbers.start_indices_batching_dims,
    )
    out = scatter_add(zeros, indices, t, scatter_dnums,
                      unique_indices=unique_indices,
                      indices_are_sorted=indices_are_sorted,
                      mode=mode)
  return [out, None]

