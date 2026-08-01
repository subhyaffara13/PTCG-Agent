
def _bcsr_dot_general_impl(lhs_data, lhs_indices, lhs_indptr, rhs, *,
                           dimension_numbers, preferred_element_type, lhs_spinfo):
  lhs_data = jnp.asarray(lhs_data)
  lhs_bcsr_indices = jnp.asarray(lhs_indices)
  lhs_bcsr_indptr = jnp.asarray(lhs_indptr)
  rhs = jnp.asarray(rhs)
  lhs_bcoo_indices = _bcsr_to_bcoo(lhs_bcsr_indices, lhs_bcsr_indptr,
                                   shape=lhs_spinfo.shape)
  return bcoo._bcoo_dot_general_impl(lhs_data, lhs_bcoo_indices, rhs,
                                     dimension_numbers=dimension_numbers,
                                     preferred_element_type=preferred_element_type,
                                     lhs_spinfo=lhs_spinfo)

