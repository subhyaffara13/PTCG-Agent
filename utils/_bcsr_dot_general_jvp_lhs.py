
def _bcsr_dot_general_jvp_lhs(lhs_data_dot, lhs_data, lhs_indices, lhs_indptr, rhs, *,
                              dimension_numbers, preferred_element_type, lhs_spinfo):
  del lhs_data
  return _bcsr_dot_general(lhs_data_dot, lhs_indices, lhs_indptr, rhs,
                           dimension_numbers=dimension_numbers,
                           preferred_element_type=preferred_element_type,
                           lhs_spinfo=lhs_spinfo)

