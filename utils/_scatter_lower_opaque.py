
def _scatter_lower_opaque(ctx, operand, indices, updates, *,
                          update_jaxpr, update_consts, dimension_numbers,
                          unique_indices, indices_are_sorted, mode):
  aval_x, aval_indices, aval_updates = ctx.avals_in
  aval_y, = ctx.avals_out
  elt_shape = core.physical_element_aval(aval_x.dtype).shape
  trailing_window_dims = [aval_updates.ndim + i for i in range(len(elt_shape))]
  dimension_numbers = dimension_numbers._replace(
      update_window_dims=(*dimension_numbers.update_window_dims,
                          *trailing_window_dims))
  scatter_lower = partial(
      _scatter_lower, update_jaxpr=update_jaxpr, update_consts=update_consts,
      dimension_numbers=dimension_numbers, unique_indices=unique_indices,
      indices_are_sorted=indices_are_sorted, mode=mode)
  res, = mlir.delegate_lowering(
      ctx, scatter_lower, operand, indices, updates,
      avals_in=[core.physical_aval(aval_x), aval_indices,
                core.physical_aval(aval_updates)],
      avals_out=[core.physical_aval(aval_y)])
  return res

