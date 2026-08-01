
def _gather_shape_computation(indices, dimension_numbers, slice_sizes):
  offset_dims = dimension_numbers.offset_dims
  collapsed_slice_dims = dimension_numbers.collapsed_slice_dims
  operand_batching_dims = dimension_numbers.operand_batching_dims
  output_shape_rank = len(offset_dims) + _rank(indices) - 1

  index_vector_dim = _rank(indices) - 1
  expanded_indices_shape = list(indices.shape)

  # This case should never happen in JAX, due to the implicit construction of
  # index_vector_dim, but is included for completeness.
  if len(expanded_indices_shape) == index_vector_dim:
    expanded_indices_shape.append(1)

  expanded_indices_shape.pop(index_vector_dim)

  indices_shape_gen = iter(expanded_indices_shape)

  slice_sizes_gen = (
      s
      for i, s in enumerate(slice_sizes)
      if i not in collapsed_slice_dims and i not in operand_batching_dims
  )
  ans = tuple(next(slice_sizes_gen) if i in offset_dims
              else next(indices_shape_gen) for i in range(output_shape_rank))
  return ans

