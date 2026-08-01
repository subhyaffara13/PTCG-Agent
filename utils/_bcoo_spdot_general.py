
def _bcoo_spdot_general(lhs_data: Array, lhs_indices: Array, rhs_data: Array, rhs_indices: Array, *,
                        lhs_spinfo: SparseInfo, rhs_spinfo: SparseInfo, dimension_numbers: DotDimensionNumbers,
                        preferred_element_type: Any) -> tuple[Array, Array]:
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  cdims = (api_util._ensure_index_tuple(lhs_contract),
           api_util._ensure_index_tuple(rhs_contract))
  bdims = (api_util._ensure_index_tuple(lhs_batch),
           api_util._ensure_index_tuple(rhs_batch))
  return bcoo_spdot_general_p.bind(lhs_data, lhs_indices, rhs_data, rhs_indices,
                                   lhs_spinfo=lhs_spinfo, rhs_spinfo=rhs_spinfo,
                                   dimension_numbers=(cdims, bdims),
                                   preferred_element_type=preferred_element_type)

