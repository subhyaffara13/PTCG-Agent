
def _clamp_scatter_indices(operand, indices, updates, *, dnums):
  """Clamps `indices` to be in-range for a scatter."""
  slice_sizes = []
  pos = 0
  for i in range(len(operand.shape)):
    if i in dnums.inserted_window_dims or i in dnums.operand_batching_dims:
      slice_sizes.append(1)
    else:
      slice_sizes.append(updates.shape[dnums.update_window_dims[pos]])
      pos += 1

  upper_bounds: core.Shape = tuple(operand.shape[i] - slice_sizes[i]
                                   for i in dnums.scatter_dims_to_operand_dims)

  # Stack upper_bounds into a Array[n]
  upper_bound = lax.shape_as_value(upper_bounds)
  # This fix fails lax_test_no_jax_array
  upper_bound = lax.min(
      upper_bound,
      upper_bound.dtype.type(
          min(np.iinfo(upper_bound.dtype).max, np.iinfo(indices.dtype).max)
      ),
  )
  upper_bound = lax.convert_element_type(upper_bound, indices.dtype)
  upper_bound = lax.broadcast_in_dim(upper_bound, indices.shape,
                                     (len(indices.shape) - 1,))
  return lax.clamp(indices.dtype.type(0), indices, upper_bound)

