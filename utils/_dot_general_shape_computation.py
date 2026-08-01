
def _dot_general_shape_computation(lhs_shape, rhs_shape, dimension_numbers):
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = _from_maybe_ragged(dimension_numbers)
  batch_shape = tuple(lhs_shape[i] for i in lhs_batch)
  lhs_contract_or_batch = tuple(sorted(tuple(lhs_contracting) + tuple(lhs_batch)))
  lhs_tensored_shape = tuple_delete(lhs_shape, lhs_contract_or_batch)
  rhs_group = ()
  if isinstance(dimension_numbers, RaggedDotDimensionNumbers):
    rhs_group = tuple(dimension_numbers.rhs_group_dimensions)
  rhs_contract_or_batch_or_group = tuple(
      sorted(tuple(rhs_contracting) + tuple(rhs_batch) + rhs_group)
  )
  rhs_tensored_shape = tuple_delete(rhs_shape, rhs_contract_or_batch_or_group)
  return batch_shape + lhs_tensored_shape + rhs_tensored_shape

