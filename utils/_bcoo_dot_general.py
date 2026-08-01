
def _bcoo_dot_general(lhs_data: Array, lhs_indices: Array, rhs: Array, *,
                      dimension_numbers: DotDimensionNumbers,
                      preferred_element_type: Any,
                      lhs_spinfo: SparseInfo) -> Array:
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  cdims = (api_util._ensure_index_tuple(lhs_contract),
           api_util._ensure_index_tuple(rhs_contract))
  bdims = (api_util._ensure_index_tuple(lhs_batch),
           api_util._ensure_index_tuple(rhs_batch))
  if preferred_element_type is not None:
    preferred_element_type = np.dtype(preferred_element_type)
  return bcoo_dot_general_p.bind(jnp.asarray(lhs_data), jnp.asarray(lhs_indices), jnp.asarray(rhs),
                                 dimension_numbers=(cdims, bdims),
                                 preferred_element_type=preferred_element_type,
                                 lhs_spinfo=lhs_spinfo)

