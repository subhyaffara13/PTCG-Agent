
def _bcoo_dot_general_jvp_rhs(rhs_dot, lhs_data, lhs_indices, rhs, *, dimension_numbers,
                              preferred_element_type, lhs_spinfo: SparseInfo):
  return _bcoo_dot_general(lhs_data, lhs_indices, rhs_dot, dimension_numbers=dimension_numbers,
                           preferred_element_type=preferred_element_type, lhs_spinfo=lhs_spinfo)

