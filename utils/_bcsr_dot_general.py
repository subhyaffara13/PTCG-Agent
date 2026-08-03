from typing import Any

def _bcsr_dot_general(lhs_data: jax.Array, lhs_indices: jax.Array,
                      lhs_indptr: jax.Array, rhs: Array, *,
                      dimension_numbers: DotDimensionNumbers,
                      preferred_element_type: Any,
                      lhs_spinfo: SparseInfo) -> Array:
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  cdims = (api_util._ensure_index_tuple(lhs_contract),
           api_util._ensure_index_tuple(rhs_contract))
  bdims = (api_util._ensure_index_tuple(lhs_batch),
           api_util._ensure_index_tuple(rhs_batch))
  return bcsr_dot_general_p.bind(jnp.asarray(lhs_data),
                                 jnp.asarray(lhs_indices),
                                 jnp.asarray(lhs_indptr), jnp.asarray(rhs),
                                 dimension_numbers=(cdims, bdims),
                                 preferred_element_type=preferred_element_type,
                                 lhs_spinfo=lhs_spinfo)

