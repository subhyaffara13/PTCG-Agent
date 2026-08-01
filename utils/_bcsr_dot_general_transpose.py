
def _bcsr_dot_general_transpose(ct, lhs_data, lhs_indices, lhs_indptr, rhs, *,
                                 dimension_numbers, preferred_element_type, lhs_spinfo):
  # TODO(jakevdp): implement this in terms of bcsr_dot_general
  lhs_bcoo_indices = _bcsr_to_bcoo(
    lhs_indices, lhs_indptr, shape=lhs_spinfo.shape)
  data_out, _, rhs_out = bcoo._bcoo_dot_general_transpose(
      ct, lhs_data, lhs_bcoo_indices, rhs, dimension_numbers=dimension_numbers,
      preferred_element_type=preferred_element_type, lhs_spinfo=lhs_spinfo)
  return data_out, lhs_indices, lhs_indptr, rhs_out

