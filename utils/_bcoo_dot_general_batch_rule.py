
def _bcoo_dot_general_batch_rule(batched_args, batch_dims, *, dimension_numbers,
                                 preferred_element_type, lhs_spinfo: SparseInfo):
  _, _, rhs = batched_args
  _, _, rhs_bdim = batch_dims
  new_lhs_data, new_lhs_indices, new_lhs_spinfo = _bcoo_batch_dims_to_front(
    batched_args[:2], batch_dims[:2], lhs_spinfo,
    batch_size=None if rhs_bdim is None else rhs.shape[rhs_bdim])
  new_dimension_numbers, result_batch_dim = _dot_general_batch_dim_nums(
      (len(lhs_spinfo.shape), rhs.ndim), (0, rhs_bdim), dimension_numbers)
  batched_out = _bcoo_dot_general(new_lhs_data, new_lhs_indices, rhs, lhs_spinfo=new_lhs_spinfo,
                                  preferred_element_type=preferred_element_type,
                                  dimension_numbers=new_dimension_numbers)
  return batched_out, result_batch_dim

