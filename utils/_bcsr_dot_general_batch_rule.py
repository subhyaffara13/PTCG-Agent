
def _bcsr_dot_general_batch_rule(batched_args, batch_dims, *,
                                 dimension_numbers, preferred_element_type,
                                 lhs_spinfo):
  *lhs_args, rhs = batched_args
  *lhs_dims, rhs_bdim = batch_dims
  new_data, new_indices, new_indptr, new_lhs_spinfo = _bcsr_batch_dims_to_front(
    lhs_args, lhs_dims, lhs_spinfo,
    batch_size=None if rhs_bdim is None else rhs.shape[rhs_bdim])
  new_dimension_numbers, result_batch_dim = _dot_general_batch_dim_nums(
      (len(lhs_spinfo.shape), rhs.ndim), (0, rhs_bdim), dimension_numbers)
  batched_out = _bcsr_dot_general(new_data, new_indices, new_indptr, rhs, lhs_spinfo=new_lhs_spinfo,
                                  dimension_numbers=new_dimension_numbers,
                                  preferred_element_type=preferred_element_type)
  return batched_out, result_batch_dim

