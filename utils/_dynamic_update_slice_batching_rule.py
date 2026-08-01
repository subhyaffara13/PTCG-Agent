
def _dynamic_update_slice_batching_rule(batched_args, batch_dims):
  # Dynamic update slice is a special case of scatter; delegate to scatter batch
  # TODO(phawkins): consider removing dynamic_update_slice, use scatter always
  operand, update, *start_idx = batched_args
  operand_bd, update_bd, *start_idx_bd = batch_dims
  update_shape = (np.shape(update) if update_bd is None
                  else tuple(np.delete(np.shape(update), update_bd)))
  dims = tuple(range(len(update_shape)))
  dnums = ScatterDimensionNumbers(
      update_window_dims=dims,
      inserted_window_dims=(),
      scatter_dims_to_operand_dims=dims,
  )
  index, index_bdim = _batch_dynamic_slice_indices(start_idx, start_idx_bd)
  return api.vmap(
    partial(scatter, dimension_numbers=dnums,
            indices_are_sorted=True, unique_indices=True,
            mode=GatherScatterMode.CLIP),
    in_axes=(operand_bd, index_bdim, update_bd),
    out_axes=0)(operand, index, update), 0

