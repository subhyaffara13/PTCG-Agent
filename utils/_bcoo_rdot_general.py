
def _bcoo_rdot_general(lhs: Array, rhs_data: Array, rhs_indices: Array, *,
                       dimension_numbers: DotDimensionNumbers,
                       preferred_element_type: Any, rhs_spinfo: SparseInfo) -> Array:
  # TODO(jakevdp): perhaps this should be part of the bcoo_dot_general primitive?
  dimension_numbers_reversed: DotDimensionNumbers = tuple(d[::-1] for d in dimension_numbers)  # pyrefly: ignore[bad-assignment]
  result = _bcoo_dot_general(rhs_data, rhs_indices, lhs, lhs_spinfo=rhs_spinfo,
                             dimension_numbers=dimension_numbers_reversed,
                             preferred_element_type=preferred_element_type)
  n_contract, n_batch = (len(d[0]) for d in dimension_numbers)
  n_swap = len(rhs_spinfo.shape) - n_contract
  permutation = (*range(n_batch), *range(n_swap, result.ndim), *range(n_batch, n_swap))
  return lax.transpose(result, permutation)

