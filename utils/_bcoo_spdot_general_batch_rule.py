
def _bcoo_spdot_general_batch_rule(batched_args, batch_dims, *, lhs_spinfo: SparseInfo, rhs_spinfo: SparseInfo,
                                   preferred_element_type, dimension_numbers):
  lhs_ndim = len(lhs_spinfo.shape)
  rhs_ndim = len(rhs_spinfo.shape)
  batch_size = max(arg.shape[dim] for arg, dim in zip(batched_args, batch_dims) if dim is not None)
  lhs_data, lhs_indices, lhs_spinfo = _bcoo_batch_dims_to_front(
    batched_args[:2], batch_dims[:2], lhs_spinfo, batch_size=batch_size)
  rhs_data, rhs_indices, rhs_spinfo = _bcoo_batch_dims_to_front(
    batched_args[2:], batch_dims[2:], rhs_spinfo, batch_size=batch_size)
  dimension_numbers, result_batch_dim = _dot_general_batch_dim_nums(
      (lhs_ndim, rhs_ndim), (0, 0), dimension_numbers)
  batched_out = _bcoo_spdot_general(lhs_data, lhs_indices, rhs_data, rhs_indices,
                                    dimension_numbers=dimension_numbers,
                                    lhs_spinfo=lhs_spinfo, rhs_spinfo=rhs_spinfo,
                                    preferred_element_type=preferred_element_type)
  return batched_out, (result_batch_dim, result_batch_dim)

