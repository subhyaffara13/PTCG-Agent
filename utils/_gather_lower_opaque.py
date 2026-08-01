
def _gather_lower_opaque(ctx, operand, indices, *,
                         dimension_numbers, slice_sizes, unique_indices,
                         indices_are_sorted, mode, fill_value) -> ir.Value:
  aval_x, aval_indices = ctx.avals_in
  aval_y, = ctx.avals_out
  elt_shape = core.physical_element_aval(aval_x.dtype).shape
  trailing_offset_dims = [aval_y.ndim + i for i in range(len(elt_shape))]
  dimension_numbers = dimension_numbers._replace(
      offset_dims=(*dimension_numbers.offset_dims, *trailing_offset_dims))
  slice_sizes = (*slice_sizes, *elt_shape)
  gather_lower = partial(
      _gather_lower, dimension_numbers=dimension_numbers,
      slice_sizes=slice_sizes, unique_indices=unique_indices,
      indices_are_sorted=indices_are_sorted, mode=mode, fill_value=fill_value)
  res, = mlir.delegate_lowering(
      ctx, gather_lower, operand, indices,
      avals_in=[core.physical_aval(aval_x), aval_indices],
      avals_out=[core.physical_aval(aval_y)])
  return res

