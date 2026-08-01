
def _scatter_batching_rule(scatter_op, axis_data, batched_args, batch_dims, *,
                           update_jaxpr, update_consts, dimension_numbers,
                           indices_are_sorted, unique_indices, mode):
  operand, indices, updates = batched_args
  operand_bdim, indices_bdim, updates_bdim = batch_dims
  if all(bdim is None for bdim in batch_dims):
    out = scatter_op.bind(
        operand, indices, updates, update_jaxpr=update_jaxpr,
        update_consts=update_consts, dimension_numbers=dimension_numbers,
        indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
        mode=mode)
    return out, None

  # move the operand batch dim to the front if it is not None, otherwise create
  # it at the front (so that we can scatter into it)
  size = next(x.shape[ax] for x, ax in zip(batched_args, batch_dims)
              if ax is not None)
  operand = batching.bdim_at_front(operand, operand_bdim, size,
                                   axis_data.explicit_mesh_axis)
  updates = batching.bdim_at_front(updates, updates_bdim, size,
                                   axis_data.explicit_mesh_axis)

  if indices_bdim is None:
    inserted_window_dims = tuple(np.add(1, dimension_numbers.inserted_window_dims))
    update_window_dims = (0,) + tuple(np.add(1, dimension_numbers.update_window_dims))
    operand_batching_dims = tuple(
        np.add(1, dimension_numbers.operand_batching_dims)
    )
    scatter_dims_to_operand_dims = tuple(np.add(1, dimension_numbers.scatter_dims_to_operand_dims))
    dnums = ScatterDimensionNumbers(
        update_window_dims=update_window_dims,
        inserted_window_dims=inserted_window_dims,
        scatter_dims_to_operand_dims=scatter_dims_to_operand_dims,
        operand_batching_dims=operand_batching_dims,
        scatter_indices_batching_dims=dimension_numbers.scatter_indices_batching_dims,
    )
    operand, indices, updates = batching.spmd_names_insert_pvary(
        operand, indices, updates)
    return scatter_op.bind(
      operand, indices, updates, dimension_numbers=dnums,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=mode, update_jaxpr=update_jaxpr, update_consts=update_consts), 0

  # see the third case in _gather_batching_rule for comparison and comments
  indices = batching.bdim_at_front(indices, indices_bdim, size,
                                   axis_data.explicit_mesh_axis)

  update_window_dims = tuple(np.add(1, dimension_numbers.update_window_dims))
  inserted_window_dims = tuple(np.add(1, dimension_numbers.inserted_window_dims))
  operand_batching_dims = (0,) + tuple(
      np.add(1, dimension_numbers.operand_batching_dims))
  scatter_indices_batching_dims = (0,) + tuple(
      np.add(1, dimension_numbers.scatter_indices_batching_dims))
  scatter_dims_to_operand_dims = tuple(
      np.add(1, dimension_numbers.scatter_dims_to_operand_dims))
  dnums = ScatterDimensionNumbers(
      update_window_dims=update_window_dims,
      inserted_window_dims=inserted_window_dims,
      scatter_dims_to_operand_dims=scatter_dims_to_operand_dims,
      operand_batching_dims=operand_batching_dims,
      scatter_indices_batching_dims=scatter_indices_batching_dims)
  return scatter_op.bind(
      operand, indices, updates, dimension_numbers=dnums,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=mode, update_jaxpr=update_jaxpr, update_consts=update_consts), 0

