
def _bcsr_dot_general_jvp_rhs(rhs_dot, lhs_data, lhs_indices, lhs_indptr, rhs, *,
                              dimension_numbers, preferred_element_type, lhs_spinfo):
  del rhs
  return _bcsr_dot_general(lhs_data, lhs_indices, lhs_indptr, rhs_dot,
                           dimension_numbers=dimension_numbers,
                           preferred_element_type=preferred_element_type,
                           lhs_spinfo=lhs_spinfo)

