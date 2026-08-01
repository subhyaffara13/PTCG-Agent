
def _gather_batching_rule(batched_args: Sequence[Array], batch_dims: Sequence[int | None], *,
                          dimension_numbers, slice_sizes, unique_indices, indices_are_sorted,
                          mode, fill_value):
  operand, indices = batched_args
  operand_bdim, indices_bdim = batch_dims

  if operand_bdim is not None and indices_bdim is None:
    operand = batching.moveaxis(operand, operand_bdim, 0)
    operand_bdim = 0
    slice_sizes = (operand.shape[0],) + slice_sizes
    offset_dims = (0,) + tuple(np.add(1, dimension_numbers.offset_dims))
    collapsed_slice_dims = tuple(np.add(1, dimension_numbers.collapsed_slice_dims))
    operand_batching_dims = tuple(
        np.add(1, dimension_numbers.operand_batching_dims)
    )
    start_index_map = tuple(np.add(1, dimension_numbers.start_index_map))
    dnums = GatherDimensionNumbers(
        offset_dims=offset_dims,
        collapsed_slice_dims=collapsed_slice_dims,
        start_index_map=start_index_map,
        operand_batching_dims=operand_batching_dims,
        start_indices_batching_dims=dimension_numbers.start_indices_batching_dims,
    )
    bdim_out = operand_bdim
    return gather(
        operand, indices, dimension_numbers=dnums,
        slice_sizes=slice_sizes,
        unique_indices=unique_indices,
        indices_are_sorted=indices_are_sorted, mode=mode,
        fill_value=fill_value), bdim_out

  elif operand_bdim is None and indices_bdim is not None:
    indices = batching.moveaxis(indices, indices_bdim, 0)
    offset_dims = tuple(1 + d for d in dimension_numbers.offset_dims)
    start_indices_batching_dims = tuple(
        np.add(1, dimension_numbers.start_indices_batching_dims)
    )
    dnums = GatherDimensionNumbers(
        offset_dims=offset_dims,
        collapsed_slice_dims=dimension_numbers.collapsed_slice_dims,
        start_index_map=dimension_numbers.start_index_map,
        operand_batching_dims=dimension_numbers.operand_batching_dims,
        start_indices_batching_dims=start_indices_batching_dims,
    )
    # If batching indexed accesses into the same array, the batched gather may
    # no longer have sorted or unique indices.
    return gather(operand, indices, dimension_numbers=dnums,
                  slice_sizes=slice_sizes, unique_indices=False,
                  indices_are_sorted=False, mode=mode, fill_value=fill_value), 0

  else:
    assert operand_bdim is not None
    assert indices_bdim is not None

    # move batch dimensions to the front to simplify logic
    operand = batching.moveaxis(operand, operand_bdim, 0)
    indices = batching.moveaxis(indices, indices_bdim, 0)

    if core.definitely_equal(operand.shape[0], 0):
      slice_sizes = (0,) + slice_sizes
    else:
      slice_sizes = (1,) + slice_sizes
    collapsed_slice_dims = tuple(
        np.add(1, dimension_numbers.collapsed_slice_dims)
    )
    operand_batching_dims = (0,) + tuple(
        np.add(1, dimension_numbers.operand_batching_dims)
    )
    start_indices_batching_dims = (0,) + tuple(
        np.add(1, dimension_numbers.start_indices_batching_dims)
    )
    offset_dims = tuple(np.add(1, dimension_numbers.offset_dims))
    start_index_map = tuple(np.add(1, dimension_numbers.start_index_map))

    dnums = GatherDimensionNumbers(
        offset_dims=offset_dims,
        collapsed_slice_dims=collapsed_slice_dims,
        start_index_map=start_index_map,
        operand_batching_dims=operand_batching_dims,
        start_indices_batching_dims=start_indices_batching_dims,
    )
    return gather(operand, indices, dimension_numbers=dnums,
                  slice_sizes=slice_sizes, unique_indices=unique_indices,
                  indices_are_sorted=indices_are_sorted, mode=mode,
                  fill_value=fill_value), 0

