import functools

def _bcoo_spdot_general_impl(lhs_data, lhs_indices, rhs_data, rhs_indices, *, lhs_spinfo: SparseInfo, rhs_spinfo: SparseInfo,
                             dimension_numbers, preferred_element_type):
  lhs_shape = lhs_spinfo.shape
  rhs_shape = rhs_spinfo.shape

  lhs = _validate_bcoo(lhs_data, lhs_indices, lhs_shape)
  rhs = _validate_bcoo(rhs_data, rhs_indices, rhs_shape)
  assert lhs.n_dense == rhs.n_dense == 0
  data_aval, _ = _bcoo_spdot_general_abstract_eval(
    lhs_data.aval, lhs_indices.aval, rhs_data.aval, rhs_indices.aval,
    lhs_spinfo=lhs_spinfo, rhs_spinfo=rhs_spinfo, dimension_numbers=dimension_numbers,
    preferred_element_type=preferred_element_type)
  out_nse = data_aval.shape[-1]

  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers

  # Move batch dimensions to front of each array.
  lhs_batch_perm = [*lhs_batch, *remaining(range(lhs.n_batch), lhs_batch)]
  rhs_batch_perm = [*rhs_batch, *remaining(range(rhs.n_batch), rhs_batch)]
  lhs_data = lhs_data.transpose([*lhs_batch_perm, *range(lhs.n_batch, lhs_data.ndim)])
  rhs_data = rhs_data.transpose([*rhs_batch_perm, *range(rhs.n_batch, rhs_data.ndim)])
  lhs_indices = lhs_indices.transpose([*lhs_batch_perm, *range(lhs.n_batch, lhs_indices.ndim)])
  rhs_indices = rhs_indices.transpose([*rhs_batch_perm, *range(rhs.n_batch, rhs_indices.ndim)])

  # Implement batched dot product via vmap
  func = functools.partial(_bcoo_spdot_general_unbatched,
      lhs_spinfo=SparseInfo(lhs_shape[lhs.n_batch:]),
      rhs_spinfo=SparseInfo(rhs_shape[rhs.n_batch:]),
      lhs_contracting=[d - lhs.n_batch for d in lhs_contracting],
      rhs_contracting=[d - rhs.n_batch for d in rhs_contracting],
      out_nse=out_nse)

  func = nfold_vmap(func, rhs.n_batch - len(rhs_batch), in_axes=(None, None, 0, 0))
  func = nfold_vmap(func, lhs.n_batch - len(lhs_batch), in_axes=(0, 0, None, None))
  func = nfold_vmap(func, len(lhs_batch))
  return func(lhs_data, lhs_indices, rhs_data, rhs_indices)

